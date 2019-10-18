import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from users.models import User
from gallery.helpers import upload_to_photo_directory


class Album(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_user', null=False, blank=False, verbose_name="Создатель")

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        ordering = ['order']



class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=upload_to_photo_directory)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        ordering = ['order']
