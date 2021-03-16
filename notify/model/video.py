from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from notify.helpers import VERB, STATUS


class VideoNotify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    list = models.ForeignKey('video.VideoAlbum', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('video.VideoComment', blank=True, null=True, on_delete=models.CASCADE)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

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
        cls.objects.filter(recipient_id=user_pk, status=UNREAD).update(status=READ)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_unread(self):
        return self.status is UNREAD


class VideoCommunityNotify(models.Model):
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='video_community_notifications', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_recipient', verbose_name="Получатель")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    list = models.ForeignKey('video.VideoAlbum', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('video.VideoComment', null=True, blank=True, on_delete=models.CASCADE)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

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
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, status=UNREAD).update(status=READ)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_unread(self):
        return self.status is UNREAD
