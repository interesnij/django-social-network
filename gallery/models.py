import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q
from gallery.helpers import upload_to_photo_directory
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community


class PhotoList(models.Model):
    MAIN, LIST, WALL, AVATAR, MANAGER, THIS_PROCESSING, PRIVATE = 'MAI', 'LIS', 'WAL', 'AVA', 'MAN', '_PRO', 'PRI'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER, THIS_CLOSED_WALL, THIS_CLOSED_AVATAR = '_CLO', '_CLOP', '_CLOM', '_CLOMA', '_CLOW', '_CLOA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(WALL, 'Фото со стены'),(AVATAR, 'Фото со страницы'), (PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),(THIS_CLOSED_WALL, 'Закрытый со стены'),(THIS_CLOSED_AVATAR, 'Закрытый со страницы'),
    )

    community = models.ForeignKey('communities.Community', related_name='photo_lists_community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_list_creator', null=False, blank=False, verbose_name="Создатель")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def __str__(self):
        return self.name

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            PhotoList.objects.create(community=instance, type=PhotoList.MAIN, name="Основной альбом", creator=instance.creator)
            PhotoList.objects.create(community=instance, type=PhotoList.AVATAR, name="Фото со страницы", creator=instance.creator)
            PhotoList.objects.create(community=instance, type=PhotoList.WALL, name="Фото со стены", creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            PhotoList.objects.create(creator=instance, type=PhotoList.MAIN, name="Основной альбом")
            PhotoList.objects.create(creator=instance, type=PhotoList.AVATAR, name="Фото со страницы")
            PhotoList.objects.create(creator=instance, type=PhotoList.WALL, name="Фото со стены")

    def get_users_ids(self):
        users = self.users.exclude(type="DE").exclude(type="BL").exclude(type="PV").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(perm="DE").exclude(perm="BL").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()
    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()
    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    def is_avatar(self):
        return self.type == self.AVATAR
    def is_wall(self):
        return self.type == self.WALL
    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] != "_"

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo
        else:
            return self.photo_list.filter(status="PUB").first()

    def get_first_photo(self):
        return self.photo_list.exclude(status__contains="_").first()

    def get_items(self):
        return self.photo_list.filter(status="PUB")
    def get_staff_items(self):
        return self.photo_list.exclude(status__contains="_")
    def get_6_items(self):
        return self.photo_list.filter(status="PUB")[:6]
    def get_6_staff_items(self):
        return self.photo_list.exclude(status__contains="_")[:6]
    def count_items(self):
        try:
            return self.photo_list.filter(status="PUB").values("pk").count()
        except:
            return 0
    def count_items_ru(self):
        count = self.count_items()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " фотография"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " фотографии"
        else:
            return str(count) + " фотографий"

    def is_not_empty(self):
        return self.photo_list.filter(status="PUB").values("pk").exists()

    def is_item_in_list(self, item_id):
        return self.photo_list.filter(pk=item_id).values("pk").exists()

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
        return cls.objects.filter(query)
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
        return cls.objects.filter(query)
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
        from common.processing.photo import get_photo_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="PHL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_photo_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="PHL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_photo_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="PHL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_photo_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="PHL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_photo_list_notify")
        get_photo_list_processing(list, PhotoList.LIST)
        return list
    def edit_list(self, name, description, order, is_public):
        from common.processing.photo import get_photo_list_processing
        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_photo_list_processing(self, PhotoList.LIST)
            self.make_publish()
        else:
            get_photo_list_processing(self, PhotoList.PRIVATE)
            self.make_private()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = PhotoList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = PhotoList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PhotoList.THIS_DELETED
        elif self.type == "PRI":
            self.type = PhotoList.THIS_DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = PhotoList.THIS_DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_list(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PhotoList.LIST
        elif self.type == "_DELP":
            self.type = PhotoList.PRIVATE
        elif self.type == "_DELM":
            self.type = PhotoList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PhotoList.THIS_CLOSED
        elif self.type == "MAI":
            self.type = PhotoList.THIS_CLOSED_MAIN
        elif self.type == "PRI":
            self.type = PhotoList.THIS_CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = PhotoList.THIS_CLOSED_MANAGER
        elif self.type == "AVA":
            self.type = PhotoList.THIS_CLOSED_AVATAR
        elif self.type == "WAL":
            self.type = PhotoList.THIS_CLOSED_WALL
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PhotoList.LIST
        elif self.type == "_CLOM":
            self.type = PhotoList.MAIN
        elif self.type == "_CLOP":
            self.type = PhotoList.PRIVATE
        elif self.type == "_CLOM":
            self.type = PhotoList.MANAGER
        elif self.type == "_CLOW":
            self.type = PhotoList.WALL
        elif self.type == "_CLOA":
            self.type = PhotoList.AVATAR
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")


class Photo(models.Model):
    THIS_PROCESSING, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = '_PRO','PUB','PRI','MAN','_DEL','_CLO'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    list = models.ManyToManyField(PhotoList, related_name="photo_list", blank=True)
    file = ProcessedImageField(format='JPEG', options={'quality': 100}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    preview = ProcessedImageField(format='JPEG', options={'quality': 60}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=102, upscale=False)])
    description = models.TextField(max_length=250, blank=True, null=True, verbose_name="Описание")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5)

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-created"]

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

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

    @classmethod
    def create_photo(cls, creator, image, list, type):
        from common.processing.photo import get_photo_processing

        photo = cls.objects.create(creator=creator,preview=image,file=image)
        list.photo_list.add(photo)
        if not list.is_private():
            get_photo_processing(photo, Photo.PUBLISHED)
            if list.community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                community_id = community.pk
                Wall.objects.create(creator_id=creator.pk, community_id=community_id, recipient_id=user_id, type=type, object_id=photo.pk, verb="ITE")
                community_send_wall(photo.pk, creator.pk, community_id, None, "create_c_photo_wall")
                for user_id in list.community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community_id, recipient_id=user_id, type=type, object_id=photo.pk, verb="ITE")
                    community_send_notify(photo.pk, creator.pk, user_id, community_id, None, "create_c_photo_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type=type, object_id=photo.pk, verb="ITE")
                user_send_wall(photo.pk, None, "create_u_photo_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type=type, object_id=photo.pk, verb="ITE")
                    user_send_notify(photo.pk, creator.pk, user_id, None, "create_u_photo_notify")
        else:
            get_photo_processing(photo, Photo.PRIVATE)
        return photo

    def is_list_exists(self):
        return self.photo_list.filter(creator=self.creator).exists()

    def get_comments(self):
        return PhotoComment.objects.filter(photo_id=self.pk, parent__isnull=True)

    def count_comments(self):
        if self.comment > 0:
            return self.comment
        else:
            return ''

    def is_avatar(self, user):
        try:
            avatar = user.get_avatar_photos().order_by('-id')[0]
            return avatar == self
        except:
            return None

    def likes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__lt=0)

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def reposts_count(self):
        if self.repost > 0:
            return self.repost
        else:
            return ''

    def window_likes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__gt=0)[0:6]

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def window_dislikes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__lt=0)[0:6]

    def get_type(self):
        return self.list.all()[0].type

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Photo.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Photo.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def delete_photo(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Photo.THIS_DELETED
        elif self.status == "PRI":
            self.status = Photo.THIS_DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Photo.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def restore_photo(self):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = Photo.PUBLISHED
        elif self.status == "_DELP":
            self.status = Photo.PRIVATE
        elif self.status == "_DELM":
            self.status = Photo.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Photo.THIS_CLOSED
        elif self.status == "PRI":
            self.status = Photo.THIS_CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Photo.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = Photo.PUBLISHED
        elif self.status == "_CLOP":
            self.status = Photo.PRIVATE
        elif self.status == "_CLOM":
            self.status = Photo.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def send_like(self, user, community):
        import json
        from common.model.votes import PhotoVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PhotoVotes.objects.get(parent=self, user=user)
            if item.vote != PhotoVotes.LIKE:
                item.vote = PhotoVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=self, user=user, vote=PhotoVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "PHO", "u_photo_notify", "LIK")
                community_wall(user, community, None, self.pk, "PHO", "u_photo_notify", "LIK")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "PHO", "u_photo_notify", "LIK")
                user_wall(user, None, self.pk, "PHO", "u_photo_notify", "LIK")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PhotoVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PhotoVotes.objects.get(parent=self, user=user)
            if item.vote != PhotoVotes.DISLIKE:
                item.vote = PhotoVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=self, user=user, vote=PhotoVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "PHO", "u_photo_notify", "DIS")
                community_wall(user, community, None, self.pk, "PHO", "u_photo_notify", "DIS")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "PHO", "u_photo_notify", "DIS")
                user_wall(user, None, self.pk, "PHO", "u_photo_notify", "DIS")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")


class PhotoComment(models.Model):
    EDITED, PUBLISHED, THIS_PROCESSING = 'EDI', 'PUB', '_PRO'
    THIS_DELETED, THIS_EDITED_DELETED = '_DEL', '_DELE'
    THIS_CLOSED, THIS_EDITED_CLOSED = '_CLO', '_CLOE'
    STATUS = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'), (THIS_EDITED_DELETED, 'Удалённый изменённый'),
        (THIS_CLOSED, 'Закрытый менеджером'), (THIS_EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='photo_comment_replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    status = models.CharField(max_length=5, choices=STATUS, default=THIS_PROCESSING, verbose_name="Тип альбома")

    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return PhotoComment.objects.filter(parent=self).all()

    def count_replies(self):
        return self.photo_comment_replies.filter(Q(status=PhotoComment.EDITED)|Q(status=PhotoComment.PUBLISHED)).values("pk").count()

    def count_replies_ru(self):
        count = self.count_replies()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def likes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)

    def window_likes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)[0:6]

    def dislikes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)

    def window_dislikes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)[0:6]

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

    def reposts_count(self):
        if self.repost > 0:
            return self.repost
        else:
            return ''

    @classmethod
    def create_comment(cls, commenter, attach, photo, parent, text, community):
        from common.notify.notify import community_wall, community_notify, user_wall, user_notify

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        comment = PhotoComment.objects.create(commenter=commenter, attach=_attach, parent=parent, photo=photo, text=text)
        photo.comment += 1
        photo.save(update_fields=["comment"])
        if comment.parent:
            if community:
                community_notify(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
                community_wall(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
            else:
                user_notify(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
                user_wall(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
        else:
            if comment.photo.community:
                community_notify(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
                community_wall(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
            else:
                user_notify(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
                user_wall(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
        return comment

    def get_u_attach(self, user):
        from common.attach.comment_attach import get_u_comment_attach
        return get_u_comment_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.comment_attach import get_c_comment_attach
        return get_c_comment_attach(self, user)

    def delete_comment(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = PhotoComment.THIS_DELETED
        elif self.status == "EDI":
            self.status = PhotoComment.THIS_EDITED_DELETED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.photo.comment -= 1
            self.parent.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.photo.comment -= 1
            self.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="C")
    def restore_comment(self):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = PhotoComment.PUBLISHED
        elif self.status == "_DELE":
            self.status = PhotoComment.EDITED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.photo.comment += 1
            self.parent.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.photo.comment += 1
            self.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = PhotoComment.THIS_CLOSED
        elif self.status == "EDI":
            self.status = PhotoComment.THIS_EDITED_CLOSED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.photo.comment -= 1
            self.parent.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.photo.comment -= 1
            self.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = PhotoComment.PUBLISHED
        elif self.status == "_CLOE":
            self.status = PhotoComment.EDITED
        self.save(update_fields=['status'])
        if self.parent:
            self.parent.photo.comment += 1
            self.parent.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.photo.comment += 1
            self.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="R")

    def send_like(self, user, community):
        import json
        from common.model.votes import PhotoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PhotoCommentVotes.objects.get(item=self, user=user)
            if item.vote != PhotoCommentVotes.LIKE:
                item.vote = PhotoCommentVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=self, user=user, vote=PhotoCommentVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LRE")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LRE")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PhotoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PhotoCommentVotes.objects.get(item=self, user=user)
            if item.vote != PhotoCommentVotes.DISLIKE:
                item.vote = PhotoCommentVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=self, user=user, vote=PhotoCommentVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DRE")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DRE")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
