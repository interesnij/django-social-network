import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q
from django.conf import settings
from gallery.helpers import upload_to_photo_directory
from common.model.votes import PhotoVotes, PhotoCommentVotes
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Album(models.Model):
    AVATAR = 'AV'
    WALL = 'WA'
    MAIN = 'MA'
    ALBUM = 'AL'
    TYPE = (
        (AVATAR, 'Фото со страницы'),
        (WALL, 'Фото со стены'),
        (MAIN, 'Основной альбом'),
        (ALBUM, 'Пользовательский альбом'),
    )

    community = models.ForeignKey('communities.Community', related_name='album_community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    type = models.CharField(max_length=5, choices=TYPE, default=MAIN, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_album_creator', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )

    users = models.ManyToManyField("users.User", blank=True, related_name='users_photolist')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='communities_photolist')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def get_users_ids(self):
        users = self.users.exclude(perm="DE").exclude(perm="BL").exclude(perm="PV").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(perm="DE").exclude(perm="BL").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        if self.creator.pk != user_id and user_id not in self.get_users_ids():
            return True
        else:
            return False
    def is_user_can_delete_list(self, user_id):
        if self.creator.pk != user_id and user_id in self.get_users_ids():
            return True
        else:
            return False
    def is_community_can_add_list(self, community_id):
        if self.community.pk != community_id and community_id not in self.get_communities_ids():
            return True
        else:
            return False
    def is_community_can_delete_list(self, community_id):
        if self.community.pk != community_id and community_id in self.get_communities_ids():
            return True
        else:
            return False

    def is_avatar_album(self):
        return self.type == self.AVATAR
    def is_wall_album(self):
        return self.type == self.WALL
    def is_main_album(self):
        return self.type == self.MAIN
    def is_user_album(self):
        return self.type == self.ALBUM

    def __str__(self):
        return self.title

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo
        else:
            return self.photo_album.filter(is_deleted=False,is_public=True).first()

    def get_first_photo(self):
        return self.photo_album.filter(is_deleted=False).first()

    def get_6_photos(self):
        return self.photo_album.filter(is_deleted=False,is_public=True)[:5]

    def get_staff_6_photos(self):
        return self.photo_album.filter(is_deleted=False)[:5]

    def count_photo(self):
        try:
            return self.photo_album.filter(is_deleted=False).values("pk").count()
        except:
            return 0
    def count_photo_ru(self):
        count = self.count_photo()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " фотография"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " фотографии"
        else:
            return str(count) + " фотографий"

    def get_photos(self):
        return self.photo_album.filter(is_deleted=False, is_public=True)

    def get_staff_photos(self):
        return self.photo_album.filter(is_deleted=False)

    def is_not_empty(self):
        return self.photo_album.filter(album=self).values("pk").exists()

    def is_photo_in_album(self, photo_id):
        return self.photo_album.filter(pk=photo_id).values("pk").exists()


class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    album = models.ManyToManyField(Album, related_name="photo_album", blank=True)
    file = ProcessedImageField(format='JPEG', options={'quality': 100}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    preview = ProcessedImageField(format='JPEG', options={'quality': 60}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=102, upscale=False)])
    description = models.TextField(max_length=250, blank=True, null=True, verbose_name="Описание")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False )
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-created"]

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def create_photo(cls, creator, album=None, file=None, community=None, created=None, is_public=None, description=None, item=None ):
        photo = Photo.objects.create(creator=creator, file=file, community=community, is_public=is_public, album=album, description=description, item=item, )
        return photo

    @classmethod
    def create_avatar(cls, creator, album=None, file=None, community=None, created=None, is_public=None, description=None):
        photo = Photo.objects.create(creator=creator, file=file, community=community, is_public=is_public, album=album, description=description,)
        return photo

    def is_album_exists(self):
        return self.photo_album.filter(creator=self.creator).exists()

    def get_comments(self):
        comments_query = Q(photo_id=self.pk)
        comments_query.add(Q(parent__isnull=True), Q.AND)
        return PhotoComment.objects.filter(comments_query)

    def count_comments(self):
        parent_comments = PhotoComment.objects.filter(photo_id=self.pk, is_deleted=False)
        parents_count = parent_comments.count()
        i = 0
        for comment in parent_comments:
            i = i + comment.count_replies()
        i = i + parents_count
        return i

    def is_avatar(self, user):
        try:
            avatar = user.get_avatar_photos().order_by('-id')[0]
            if avatar == self:
                return True
            else:
                return None
        except:
            return None

    def likes(self):
        likes = PhotoVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def likes_count(self):
        likes = PhotoVotes.objects.filter(parent=self, vote__gt=0).values("pk").count()
        if likes > 0:
            return likes
        else:
            return ''

    def window_likes(self):
        likes = PhotoVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = PhotoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def dislikes_count(self):
        dislikes = PhotoVotes.objects.filter(parent=self, vote__lt=0).values("pk").count()
        if dislikes > 0:
            return dislikes
        else:
            return ''

    def window_dislikes(self):
        dislikes = PhotoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes[0:6]

    def delete_photo(self):
        try:
            from notify.models import Notify
            n = Notify.objects.get(creator=self.creator, verb="ITE", attach="pho" + str(self.pk))
            n.status = "C"
            n.save(update_fields=['status'])
        except:
            pass
        self.is_deleted = True
        return self.save(update_fields=['is_deleted'])

    def abort_delete_photo(self):
        try:
            from notify.models import Notify
            n = Notify.objects.get(creator=self.creator, verb="ITE", attach="pho" + str(self.pk))
            n.status = "R"
            n.save(update_fields=['status'])
        except:
            pass
        self.is_deleted = False
        return self.save(update_fields=['is_deleted'])


class PhotoComment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='photo_comment_replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    id = models.BigAutoField(primary_key=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")

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
        get_comments = PhotoComment.objects.filter(parent=self).all()
        return get_comments

    def count_replies(self):
        return self.photo_comment_replies.filter(is_deleted=False).values("pk").count()

    def count_replies_ru(self):
        count = self.photo_comment_replies.filter(is_deleted=False).values("pk").count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def likes(self):
        likes = PhotoCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)
        return likes

    def window_likes(self):
        likes = PhotoCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = PhotoCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = PhotoCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)
        return dislikes[0:6]

    def __str__(self):
        return self.text

    def likes_count(self):
        likes = PhotoCommentVotes.objects.filter(item=self, vote__gt=0).values("pk").count()
        if likes > 0:
            return likes
        else:
            return ''

    def dislikes_count(self):
        dislikes = PhotoCommentVotes.objects.filter(item=self, vote__lt=0).values("pk").count()
        if dislikes > 0:
            return dislikes
        else:
            return ''

    @classmethod
    def create_comment(cls, commenter, attach, photo, parent, text):
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        comment = PhotoComment.objects.create(commenter=commenter, attach=_attach, parent=parent, photo=photo, text=text, created=timezone.now())
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "comment_item",
            "actor_name": comment.commenter.get_full_name()
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return comment

    def get_u_attach(self, user):
        from common.attach.comment_attach import get_u_comment_attach
        return get_u_comment_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.comment_attach import get_c_comment_attach
        return get_c_comment_attach(self, user)
