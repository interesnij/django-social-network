import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from users.models import User
from gallery.helpers import upload_to_photo_directory
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from django.contrib.contenttypes.fields import GenericRelation


class Album(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='albums')
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_user', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        ordering = ['order']
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'


class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='photos')
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE)
    file = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_photo_directory, processors=[ResizeToFit(width=1024, upscale=False)])
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        ordering = ['order']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
