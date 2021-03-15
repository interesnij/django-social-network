import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from notify.helpers import NOTIFICATION_TYPES


class VideoNotify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('video.VideoAlbum', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('video.VideoComment', blank=True, null=True, on_delete=models.CASCADE)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Уведомление - ролики пользователя"
        verbose_name_plural = "Уведомления - ролики пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.video and not self.comment:
            return '{} {} {}'.format(self.creator, self.get_verb_display(), self.video)
        else:
            return '{} {} {} {}'.format(self.creator, self.get_verb_display(), self.comment, self.video)

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


class VideoCommunityNotify(models.Model):
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='video_community_notifications', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_recipient', verbose_name="Получатель")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('video.VideoAlbum', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('video.VideoComment', null=True, blank=True, on_delete=models.CASCADE)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Уведомление - ролики сообщества"
        verbose_name_plural = "Уведомления - ролики сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.video and not self.video_comment:
            return '{} {} {}'.format(self.creator, self.get_verb_display(), self.video)
        else:
            return '{} {} {} {}'.format(self.creator, self.get_verb_display(), self.video_comment, self.video)

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)
