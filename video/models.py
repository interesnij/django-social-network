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
    MAIN, LIST, MANAGER, THIS_PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', 'TPRO', 'PRI'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = 'TDEL', 'TDELP', 'TDELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER = 'TCLO', 'TCLOP', 'TCLOM', 'TCLOMA'
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

    #@receiver(post_save, sender=settings.COMMUNITY_MODEL)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            community=instance
            VideoList.objects.create(community=community, type=VideoList.MAIN, name="Основной список", order=0, creator=community.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            VideoList.objects.create(creator=instance, type=VideoList.MAIN, name="Основной список", order=0)

    def is_not_empty(self):
        return self.video_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").exists()

    def get_staff_items(self):
        return self.video_listfilter(Q(status="PUB")|Q(status="PRI"))
    def get_items(self):
        return self.video_list.filter(status="PUB")
    def get_manager_items(self):
        return self.video_list.filter(status="MAN")
    def count_items(self):
        return self.video_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
    def is_user_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.LIST or self.type == self.MAIN or self.type == self.MANAGER

    def get_users_ids(self):
        users = self.users.exclude(type__contains="THIS").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="THIS").values("pk")
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
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_user_staff_lists(cls, user_pk):
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_user_lists(cls, user_pk):
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(type="LIS")
        query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(community_id=user_pk)|Q(communities__id=user_pk)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_community_staff_lists(cls, community_pk):
        query = Q(type="LIS") | Q(type="PRI")
        query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(type="LIS")
        query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_community_lists(cls, community_pk):
        query = Q(type="LIS")
        query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(type="LIS")
        query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
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
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VIL", object_id=list.pk, verb="ITE")
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
    def abort_delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "TDEL":
            self.type = VideoList.LIST
        elif self.type == "TDELP":
            self.type = VideoList.PRIVATE
        elif self.type == "TDELM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def close_list(self):
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
    def abort_close_list(self):
        from notify.models import Notify, Wall
        if self.type == "TCLO":
            self.type = VideoList.LIST
        elif self.type == "TCLOM":
            self.type = VideoList.MAIN
        elif self.type == "TCLOP":
            self.type = VideoList.PRIVATE
        elif self.type == "TCLOM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")


class Video(models.Model):
    THIS_PROCESSING, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = 'PRO','PUB','PRI','MAN','TDEL','TCLO'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = 'TDELP','TDELM','TCLOP','TCLOM'
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

    comments = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    views = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    likes = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    reposts = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        verbose_name = "Видео-ролики"
        verbose_name_plural = "Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def likes(self):
        likes = VideoVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = VideoVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = VideoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = VideoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes[0:6]

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
        likes = VideoVotes.objects.filter(parent=self, vote__gt=0).values("pk").count()
        if likes > 0:
            return likes
        else:
            return ''

    def dislikes_count(self):
        dislikes = VideoVotes.objects.filter(parent=self, vote__lt=0).values("pk").count()
        if dislikes > 0:
            return dislikes
        else:
            return ''

    def count_comments(self):
        parent_comments = VideoComment.objects.filter(video_id=self.pk, is_deleted=False).values("pk").count()
        parents_count = parent_comments.count()
        i = 0
        for comment in parent_comments:
            i = i + comment.count_replies()
        i = i + parents_count
        return i

    def get_comments(self):
        comments_query = Q(video_id=self.pk)
        comments_query.add(Q(parent__isnull=True), Q.AND)
        return VideoComment.objects.filter(comments_query)

    def get_lists_for_video(self):
        return self.list.all()
    def get_list_uuid(self):
        return self.list.all()[0].uuid

    @classmethod
    def create_video(cls, creator, title, file, uri, lists, is_public):
        #from notify.models import Notify, Wall, get_user_managers_ids
        #from common.notify import send_notify_socket
        from common.processing.video import get_video_processing
        from rest_framework.exceptions import ValidationError

        if not lists:
            raise ValidationError("Не выбран список для нового ролика")

        video = cls.objects.create(creator=creator,title=title,file=file,uri=uri)
        if is_public:
            get_video_processing(video, Video.PUBLISHED)
            #for user_id in creator.get_user_news_notify_ids():
            #    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                #send_notify_socket(object_id, user_id, "create_video_notify")
            #Wall.objects.create(creator_id=creator.pk, type="VID", object_id=video.pk, verb="ITE")
            #send_notify_socket(object_id, user_id, "create_video_wall")
        else:
            get_video_processing(video, VIDEO.PRIVATE)
        for list_id in lists:
            video_list = VIDEO.objects.get(pk=list_id)
            video_list.video_list.add(video)
        return video

    def edit_video(self, title, file, uri, lists, is_public):
        from common.processing.video import get_video_processing

        self.title = title
        self.file = file
        self.uri = uri
        self.lists = lists
        if is_public:
            get_video_processing(self, VIDEO.PUBLISHED)
            self.make_publish()
        else:
            get_video_processing(self, VIDEO.PRIVATE)
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

    def delete_video(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Video.THIS_DELETED
        elif self.status == "PRI":
            self.status = Video.THIS_DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Video.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_delete_video(self):
        from notify.models import Notify, Wall
        if self.status == "TDEL":
            self.status = Video.PUBLISHED
        elif self.status == "TDELP":
            self.status = Video.PRIVATE
        elif self.status == "TDELM":
            self.status = Video.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def close_video(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Video.THIS_CLOSED
        elif self.status == "PRI":
            self.status = Video.THIS_CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Video.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_video(self):
        from notify.models import Notify, Wall
        if self.status == "TCLO":
            self.status = Video.PUBLISHED
        elif self.status == "TCLOP":
            self.status = Video.PRIVATE
        elif self.status == "TCLOM":
            self.status = Video.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED


class VideoComment(models.Model):
    EDITED, PUBLISHED, THIS_PROCESSING = 'EDI', 'PUB', 'PRO'
    THIS_DELETED, THIS_EDITED_DELETED = 'TDEL', 'TDELE'
    THIS_CLOSED, THIS_EDITED_CLOSED = 'TCLO', 'TCLOE'
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

    likes = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    reposts = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к ролику"
        verbose_name_plural = "комментарии к ролику"

    def all_visits_count(self):
        from stst.models import VideoNumbers
        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return self.video_comment_replies.filter(Q(status="PUB")|Q(status="EDI")).all()

    def count_replies(self):
        return self.video_comment_replies.filter(Q(status="PUB")|Q(status="EDI")).values("pk").count()

    def likes(self):
        likes = VideoCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes

    def likes_count(self):
        likes = VideoVotes.objects.filter(parent=self, vote__gt=0).values("pk").count()
        if likes > 0:
            return likes
        else:
            return ''

    def dislikes_count(self):
        dislikes = VideoVotes.objects.filter(parent=self, vote__lt=0).values("pk").count()
        if dislikes > 0:
            return dislikes
        else:
            return ''

    def window_likes(self):
        likes = VideoCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = VideoCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = VideoCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes[0:6]

    def likes_count(self):
        likes = VideoCommentVotes.objects.filter(item=self, vote__gt=0).values("pk")
        return likes.count()

    def dislikes_count(self):
        dislikes = VideoCommentVotes.objects.filter(item=self, vote__lt=0).values("pk")
        return dislikes.count()

    @classmethod
    def create_comment(cls, commenter, attach, video, parent, text):
        from common.notify.notify import community_wall, community_notify, user_wall, user_notify
        from django.utils import timezone

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        comment = VideoComment.objects.create(commenter=commenter, attach=_attach, parent=parent, video=video, text=text, created=timezone.now())
        if comment.parent:
            video = comment.parent.video
            type = "vir"+str(comment.pk)+",vic"+str(comment.parent.pk)+",vid"+str(video.pk)
            if video.community:
                community_wall(commenter, community, None, type, "c_video_comment_notify", "REP")
                community_notify(commenter, community, None, type, "c_video_comment_notify", "REP")
            else:
                user_wall(commenter, None, type, "u_video_comment_notify", "REP")
                user_notify(commenter, video.creator.pk, None, type, "u_post_comment_notify", "REP")
        else:
            type = "vic"+str(comment.pk)+", vid"+str(video.pk)
            if comment.video.community:
                community_wall(commenter, community, None, type, "c_video_comment_notify", "COM")
                community_notify(commenter, community, None, type, "c_video_comment_notify", "COM")
            else:
                user_wall(commenter, None, type, "u_video_comment_notify", "COM")
                user_notify(commenter, video.creator.pk, None, type, "u_video_comment_notify", "COM")
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

    def delete_comment(self):
        try:
            from notify.models import Notify
            if self.parent:
                Notify.objects.filter(attach="vir" + str(self.pk)).update(status="C")
            else:
                Notify.objects.filter(attach="vic" + str(self.pk)).update(status="C")
        except:
            pass
        self.is_deleted = True
        return self.save(update_fields=['is_deleted'])

    def abort_delete_comment(self):
        try:
            from notify.models import Notify
            if self.parent:
                Notify.objects.filter(attach="vir" + str(self.pk)).update(status="R")
            else:
                Notify.objects.filter(attach="vic" + str(self.pk)).update(status="R")
        except:
            pass
        self.is_deleted = False
        return self.save(update_fields=['is_deleted'])
