import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from gallery.helpers import upload_to_photo_directory
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from common.models import Emoji
from main.models import Item


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


class PhotoComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def notification_comment(self, user):
        notification_handler(user, self.commenter,Notification.POST_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_reply_comment(self, user):
        notification_handler(user, self.commenter,Notification.POST_COMMENT_REPLY, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_comment_react(self, user):
        notification_handler(user, self.reactor,Notification.REACT_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')

    def get_emoji_for_post_comment(self, emoji_id=None, reactor_id=None):
        return Emoji.get_emoji_comment(post_comment_id=self, emoji_id=emoji_id,
                                                               reactor_id=reactor_id)



class PhotoReaction(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_reactions')
    created = models.DateTimeField(editable=False)
    reactor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_reactions')
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='photo_reactions')

    class Meta:
        unique_together = ('reactor', 'photo', 'emoji')
        verbose_name="реакция к записи"
        verbose_name_plural="реакции к записям"

    @classmethod
    def count_reactions_for_post_with_id(cls, photo, reactor_id=None):
        count_query = Q(photo=photo, reactor__is_deleted=False)

        if reactor_id:
            count_query.add(Q(reactor_id=reactor_id), Q.AND)

        return cls.objects.filter(count_query).count()

    def __str__(self):
        return "{0}/{1}".format(self.photo.creator.get_full_name(), self.emoji.keyword)

    def get_reactor(self):
        reactors = User.objects.filter(pk=self.reactor.pk).all()
        return reactors

    def notification_react(self, user):
        notification_handler(user, self.reactor,Notification.REACT, action_object=self,id_value=str(self.id),key='social_update')


class PhotoCommentReaction(models.Model):
    photo_comment = models.ForeignKey(PhotoComment, on_delete=models.CASCADE, related_name='photo_reactions')
    created = models.DateTimeField(editable=False)
    reactor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_comment_reactions')
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='photo_comment_reactions')

    class Meta:
        unique_together = ('reactor', 'photo_comment','emoji')
        verbose_name="реакция на комментарий"
        verbose_name_plural="реакции на комментарии"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(PhotoCommentReaction, self).save(*args, **kwargs)
