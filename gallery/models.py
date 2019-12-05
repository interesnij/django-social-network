import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from os.path import splitext
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from main.models import Item
from notifications.model.photo import *


class Album(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='albums')
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    is_generic = models.BooleanField(default=False, verbose_name="Сгенерированный альбом")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_user', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def __str__(self):
        return self.title


class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='photos')
    album = models.ForeignKey(Album, related_name="album_1", blank=True, null=True, on_delete=models.CASCADE)
    album_2 = models.ForeignKey(Album, related_name="album_2", blank=True, null=True, on_delete=models.CASCADE)
    file = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_photo_directory, processors=[ResizeToFit(width=1024, upscale=False)])
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def upload_to_photo_directory(self, filename):
        extension = splitext(filename)[1].lower()
        new_filename = str(uuid.uuid4()) + extension

        path = 'photos/%(creator_id)s/' % {
            'user_id': str(self.creator.id)}

        return '%(path)s%(new_filename)s' % {'path': path,
                                             'new_filename': new_filename, }

    @classmethod
    def create_photo(cls, creator, album_2=None, file=None, community=None,
                    created=None, is_public=False, description=None, item=None ):
        photo = Photo.objects.create(
                                        creator=creator,
                                        file=file,
                                        community=community,
                                        is_public=is_public,
                                        album_2=album_2,
                                        description=description,
                                        item=item,
                                    )
        return photo

    def notification_user_repost(self, user):
        photo_notification_handler(user, self.creator, PhotoNotification.REPOST, key='social_update', photo=self)

    def notification_user_like(self, user):
        photo_notification_handler(user, self.creator, PhotoNotification.LIKE, key='social_update', photo=self)

    def notification_user_dislike(self, user):
        photo_notification_handler(user, self.creator, PhotoNotification.DISLIKE, key='social_update', photo=self)

    def notification_community_repost(self, user):
        photo_community_notification_handler(user, self.creator, PhotoCommunityNotification.REPOST, key='social_update', photo=self)

    def notification_community_like(self, user):
        photo_community_notification_handler(user, self.creator, PhotoCommunityNotification.LIKE, key='social_update', photo=self)

    def notification_community_dislike(self, user):
        photo_community_notification_handler(user, self.creator, PhotoCommunityNotification.DISLIKE, key='social_update', photo=self)


class PhotoComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='photo_comment')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def notification_user_comment(self, user):
        photo_notification_handler(user, self.commenter, PhotoNotification.POST_COMMENT, key='social_update', photo=self.photo)

    def notification_user_reply_comment(self, user):
        photo_notification_handler(user, self.commenter, PhotoNotification.POST_COMMENT_REPLY, key='social_update', photo=self.photo)

    def notification_user_comment_like(self, user):
        photo_notification_handler(user, self.commenter, PhotoNotification.LIKE_COMMENT, key='social_update', photo=self.photo)

    def notification_user_comment_dislike(self, user):
        photo_notification_handler(user, self.commenter, PhotoNotification.DISLIKE_COMMENT, key='social_update', photo=self.photo)

    def notification_community_comment(self, user):
        photo_community_notification_handler(user, self.commenter, PhotoCommunityNotification.POST_COMMENT, key='social_update', photo=self.photo)

    def notification_community_reply_comment(self, user):
        photo_community_notification_handler(user, self.commenter, PhotoCommunityNotification.POST_COMMENT_REPLY, key='social_update', photo=self.photo)

    def notification_community_comment_like(self, user):
        photo_community_notification_handler(user, self.commenter, PhotoCommunityNotification.LIKE_COMMENT, key='social_update', photo=self.photo)

    def notification_community_comment_dislike(self, user):
        photo_community_notification_handler(user, self.commenter, PhotoCommunityNotification.DISLIKE_COMMENT, key='social_update', photo=self.photo)
