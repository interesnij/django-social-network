from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from notify.helpers import VERB, STATUS


class PhotoNotify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    photo = models.ForeignKey('gallery.Photo', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('gallery.Album', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('gallery.PhotoComment', blank=True, null=True, on_delete=models.CASCADE)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление - фотографии пользователя"
        verbose_name_plural = "Уведомления - фотографии пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_unread(self):
        return self.status is UNREAD

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, status=UNREAD).update(status=READ)

class PhotoCommunityNotify(models.Model):
    community = models.ForeignKey('communities.Community', related_name='community_photo_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_photo_recipient', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    photo = models.ForeignKey('gallery.Photo', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('gallery.Album', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('gallery.PhotoComment', null=True, blank=True, on_delete=models.CASCADE)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление - фотографии сообщества"
        verbose_name_plural = "Уведомления - фотографии сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    def is_unread(self):
        return self.status is UNREAD

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, status=UNREAD).update(status=READ)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)
