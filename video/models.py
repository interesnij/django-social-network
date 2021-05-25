import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from video.helpers import upload_to_video_directory, validate_file_extension
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_videos_count(self):
        return self.video_category.filter(is_deleted=True).values("pk").count()

    def is_video_in_category(self, track_id):
        self.video_category.filter(id=track_id).exists()

    def get_100_videos(self):
        queryset = self.video_category.filter(is_deleted=True).values("pk").count()
        return queryset[:100]

    class Meta:
        verbose_name = "Категория ролика"
        verbose_name_plural = "Категории ролика"


class VideoList(models.Model):
    MAIN, LIST, MANAGER, THIS_PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    community = models.ForeignKey('communities.Community', related_name='video_lists_community', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    name = models.CharField(max_length=250, verbose_name="Название")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_creator', verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    class Meta:
        verbose_name = 'Видеоальбом'
        verbose_name_plural = 'Видеоальбомы'
        ordering = ['order']

    def __str__(self):
        return self.title

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            VideoList.objects.create(community=instance, type=VideoList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            VideoList.objects.create(creator=instance, type=VideoList.MAIN, name="Основной список", order=0)

    def is_not_empty(self):
        return self.video_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").exists()

    def get_staff_items(self):
        return self.video_list.filter(Q(status="PUB")|Q(status="PRI"))
    def get_items(self):
        return self.video_list.filter(status="PUB")
    def get_manager_items(self):
        return self.video_list.filter(status="MAN")
    def count_items(self):
        return self.video_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").count()

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.LIST or self.type == self.MAIN or self.type == self.MANAGER

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()
    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()
    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.video import get_video_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="VIL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_video_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VIL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_video_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="VIL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_video_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VIL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_video_list_notify")
        get_video_list_processing(list, VideoList.LIST)
        return list

    def edit_list(self, name, description, order, is_public):
        from common.processing.video import get_video_list_processing

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_video_list_processing(self, VideoList.LIST)
            self.make_publish()
        else:
            get_video_list_processing(self, VideoList.PRIVATE)
            self.make_private()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = VideoList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = VideoList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoList.THIS_DELETED
        elif self.type == "PRI":
            self.type = VideoList.THIS_DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = VideoList.THIS_DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_list(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = VideoList.LIST
        elif self.type == "_DELP":
            self.type = VideoList.PRIVATE
        elif self.type == "_DELM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoList.THIS_CLOSED
        elif self.type == "MAI":
            self.type = VideoList.THIS_CLOSED_MAIN
        elif self.type == "PRI":
            self.type = VideoList.THIS_CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = VideoList.THIS_CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = VideoList.LIST
        elif self.type == "_CLOM":
            self.type = VideoList.MAIN
        elif self.type == "_CLOP":
            self.type = VideoList.PRIVATE
        elif self.type == "_CLOM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")


class Video(models.Model):
    THIS_PROCESSING, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = '_PRO','PUB','PRI','MAN','_DEL','_CLO'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    image = ProcessedImageField(format='JPEG',
                                options={'quality': 90},
                                upload_to=upload_to_video_directory,
                                processors=[ResizeToFit(width=500, upscale=False)],
                                verbose_name="Обложка")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    title = models.CharField(max_length=255, verbose_name="Название")
    uri = models.CharField(max_length=255, verbose_name="Ссылка на видео")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    list = models.ManyToManyField(VideoList, related_name="video_list", blank=True, verbose_name="Альбом")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_creator", on_delete=models.CASCADE, verbose_name="Создатель")
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5)
    file = models.FileField(blank=True, upload_to=upload_to_video_directory, validators=[validate_file_extension], verbose_name="Видеозапись")
    community = models.ForeignKey('communities.Community', related_name='video_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        verbose_name = "Видео-ролики"
        verbose_name_plural = "Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def __str__(self):
        return self.name

    def plus_likes(self, count):
        self.like += count
        return self.save(update_fields=['like'])
    def minus_likes(self, count):
        self.like -= count
        return self.save(update_fields=['like'])
    def plus_dislikes(self, count):
        self.dislike += count
        return self.save(update_fields=['dislike'])
    def minus_dislikes(self, count):
        self.dislike -= count
        return self.save(update_fields=['dislike'])
    def plus_comments(self, count):
        self.comment += count
        return self.save(update_fields=['comment'])
    def minus_comments(self, count):
        self.comment -= count
        return self.save(update_fields=['comment'])
    def plus_views(self, count):
        self.view += count
        return self.save(update_fields=['view'])
    def minus_views(self, count):
        self.view -= count
        return self.save(update_fields=['view'])
    def plus_reposts(self, count):
        self.repost += count
        return self.save(update_fields=['repost'])
    def minus_reposts(self, count):
        self.repost -= count
        return self.save(update_fields=['repost'])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def likes(self):
        return VideoVotes.objects.filter(parent=self, vote__gt=0)

    def window_likes(self):
        return VideoVotes.objects.filter(parent=self, vote__gt=0)[0:6]

    def dislikes(self):
        return VideoVotes.objects.filter(parent=self, vote__lt=0)

    def window_dislikes(self):
        return VideoVotes.objects.filter(parent=self, vote__lt=0)[0:6]

    def visits_count_ru(self):
        count = self.all_visits_count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " просмотра"
        else:
            return str(count) + " просмотров"

    def all_visits_count(self):
        from stst.models import VideoNumbers
        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def count_comments(self):
        if self.comment > 0:
            return self.comment
        else:
            return ''

    def get_comments(self):
        return VideoComment.objects.filter(video_id=self.pk, parent__isnull=True)

    def get_lists_for_video(self):
        return self.list.all()
    def get_list_uuid(self):
        return self.list.all()[0].uuid

    @classmethod
    def create_video(cls, creator, title, file, uri, description, lists, comments_enabled, votes_on, is_public, community):
        from common.processing.video import get_video_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")
        private = 0
        video = cls.objects.create(creator=creator,title=title,file=file,uri=uri,description=description, comments_enabled=comments_enabled, votes_on=votes_on)
        if community:
            community.plus_videos(1)
        else:
            creator.plus_videos(1)
        for list_id in lists:
            video_list = VideoList.objects.get(pk=list_id)
            video_list.video_list.add(video)
            if video_list.is_private():
                private = 1
        if not private and is_public:
            get_video_processing(video, Video.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                community_send_wall(video.pk, creator.pk, community.pk, None, "create_c_video_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                    community_send_notify(video.pk, creator.pk, user_id, community.pk, None, "create_c_video_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type="VID", object_id=video.pk, verb="ITE")
                user_send_wall(video.pk, None, "create_u_video_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                    user_send_notify(video.pk, creator.pk, user_id, None, "create_u_video_notify")
        else:
            get_video_processing(video, Video.PRIVATE)
        return video

    def edit_video(self, title, file, uri, description, lists, comments_enabled, votes_on, is_public):
        from common.processing.video import get_video_processing

        self.title = title
        self.file = file
        self.uri = uri
        self.lists = lists
        self.description = description
        self.comments_enabled = comments_enabled
        self.votes_on = votes_on
        if is_public:
            get_video_processing(self, Video.PUBLISHED)
            self.make_publish()
        else:
            get_video_processing(self, Video.PRIVATE)
            self.make_private()
        return self.save()

    def get_uri(self):
        if self.file:
            return self.file.url
        else:
            return self.uri

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Video.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Video.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def delete_video(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Video.THIS_DELETED
        elif self.status == "PRI":
            self.status = Video.THIS_DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Video.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_videos(1)
        else:
            self.creator.minus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def restore_video(self, community):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = Video.PUBLISHED
        elif self.status == "_DELP":
            self.status = Video.PRIVATE
        elif self.status == "_DELM":
            self.status = Video.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_videos(1)
        else:
            self.creator.plus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Video.THIS_CLOSED
        elif self.status == "PRI":
            self.status = Video.THIS_CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Video.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_videos(1)
        else:
            self.creator.minus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = Video.PUBLISHED
        elif self.status == "_CLOP":
            self.status = Video.PRIVATE
        elif self.status == "_CLOM":
            self.status = Video.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_videos(1)
        else:
            self.creator.plus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED


class VideoComment(models.Model):
    EDITED, PUBLISHED, THIS_PROCESSING = 'EDI', 'PUB', '_PRO'
    THIS_DELETED, THIS_EDITED_DELETED = '_DEL', '_DELE'
    THIS_CLOSED, THIS_EDITED_CLOSED = '_CLO', '_CLOE'
    STATUS = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'), (THIS_EDITED_DELETED, 'Удалённый изменённый'),
        (THIS_CLOSED, 'Закрытый менеджером'), (THIS_EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='video_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    status = models.CharField(max_length=5, choices=STATUS, default=THIS_PROCESSING, verbose_name="Тип альбома")

    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к ролику"
        verbose_name_plural = "комментарии к ролику"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def all_visits_count(self):
        from stst.models import VideoNumbers
        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return self.video_comment_replies.filter(Q(status=VideoComment.EDITED)|Q(status=VideoComment.PUBLISHED)).only("pk")

    def count_replies(self):
        return self.video_comment_replies.filter(Q(status=VideoComment.EDITED)|Q(status=VideoComment.PUBLISHED)).values("pk").count()

    def likes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__gt=0)

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def window_likes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__gt=0)[0:6]

    def dislikes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__lt=0)

    def window_dislikes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__lt=0)[0:6]

    @classmethod
    def create_comment(cls, commenter, attach, video, parent, text, community):
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        comment = VideoComment.objects.create(commenter=commenter, attach=_attach, parent=parent, video=video, text=text)
        video.comment += 1
        video.save(update_fields=["comment"])
        if parent:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
                community_wall(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
                user_wall(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
        else:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
                community_wall(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
                user_wall(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
        return comment

    def count_replies_ru(self):
        count = self.video_comment_replies.filter(Q(status="PUB")|Q(status="EDI")).values("pk").count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def get_u_attach(self, user):
        from common.attach.comment_attach import get_u_comment_attach
        return get_u_comment_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.comment_attach import get_c_comment_attach
        return get_c_comment_attach(self, user)

    def send_like(self, user, community):
        import json
        from common.model.votes import VideoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = VideoCommentVotes.objects.get(item=self, user=user)
            if item.vote != VideoCommentVotes.LIKE:
                item.vote = VideoCommentVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=self, user=user, vote=VideoCommentVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LRE")
                    community_wall(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "LRE")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "LCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LCO")
                    community_wall(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "LCO")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "LCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import VideoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = VideoCommentVotes.objects.get(item=self, user=user)
            if item.vote != VideoCommentVotes.DISLIKE:
                item.vote = VideoCommentVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=self, user=user, vote=VideoCommentVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DRE")
                    community_wall(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "DRE")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                    community_wall(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    def delete_comment(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = VideoComment.THIS_DELETED
        elif self.status == "EDI":
            self.status = VideoComment.THIS_EDITED_DELETED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.video.comment -= 1
            self.parent.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.video.comment -= 1
            self.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="C")
    def restore_comment(self):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = VideoComment.PUBLISHED
        elif self.status == "_DELE":
            self.status = VideoComment.EDITED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.video.comment += 1
            self.parent.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.video.comment += 1
            self.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = VideoComment.THIS_CLOSED
        elif self.status == "EDI":
            self.status = VideoComment.THIS_EDITED_CLOSED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.video.comment -= 1
            self.parent.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.video.comment -= 1
            self.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = VideoComment.PUBLISHED
        elif self.status == "_CLOE":
            self.status = VideoComment.EDITED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.video.comment += 1
            self.parent.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.video.comment += 1
            self.video.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="R")
