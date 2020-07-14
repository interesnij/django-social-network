import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class VideoNotificationQS(models.query.QuerySet):
    def unread(self):
        return self.filter(unread=True)
    def read(self):
        return self.filter(unread=False)
    def mark_all_as_read(self, recipient=None):
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        qs = self.read()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=True)

    def serialize_latest_notifications(self, recipient=None):
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]
        notification_dic = serializers.serialize("json", qs)
        return notification_dic

    def get_most_recent(self, recipient=None):
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]
        return qs


class VideoNotification(models.Model):
    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    POST_USER_MENTION = 'PUM'
    POST_COMMENT_USER_MENTION = 'PCUM'
    REPOST = 'R'
    LIKE = 'L'
    DISLIKE = 'D'
    LIKE_REPLY_COMMENT = 'LRC'
    DISLIKE_REPLY_COMMENT = 'DRC'
    LIKE_COMMENT =  'LC'
    DISLIKE_COMMENT =  'DC'

    NOTIFICATION_TYPES = (
        (POST_COMMENT, 'оставил комментарий к ролику'),
        (POST_COMMENT_REPLY, 'ответил на Ваш комментарий к ролику'),
        (LIKE, 'понравилась Ваш ролик'),
        (DISLIKE, 'не понравилась Ваш ролик'),
        (LIKE_COMMENT, 'понравился Ваш комментарий к ролику'),
        (DISLIKE_COMMENT, 'не понравился Ваш комментарий к ролику'),
        (LIKE_REPLY_COMMENT, 'понравился Ваш ответ на комментарий  к ролику'),
        (DISLIKE_REPLY_COMMENT, 'не понравился Ваш ответ к комментарий к ролику'),
        (REPOST, 'поделился Вашим роликом'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_notifications', verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    objects =  VideoNotificationQS.as_manager()
    video = models.ForeignKey('video.Video', blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('video.VideoComment', blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - ролики пользователя"
        verbose_name_plural = "Уведомления - ролики пользователя"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        if self.video and not self.comment:
            return '{} {} {}'.format(self.actor, self.get_verb_display(), self.video)
        else:
            return '{} {} {} {}'.format(self.actor, self.get_verb_display(), self.comment, self.video)

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


class VideoCommunityNotification(models.Model):
    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    COMMUNITY_INVITE = 'CI'
    POST_USER_MENTION = 'PUM'
    POST_COMMENT_USER_MENTION = 'PCUM'
    REPOST = 'R'
    LIKE = 'L'
    DISLIKE = 'D'
    LIKE_REPLY_COMMENT = 'LRC'
    DISLIKE_REPLY_COMMENT = 'DRC'
    LIKE_COMMENT =  'LC'
    DISLIKE_COMMENT =  'DC'

    NOTIFICATION_TYPES = (
        (POST_COMMENT, 'оставил комментарий к записи сообщества'),
        (POST_COMMENT_REPLY, 'ответил на комментарий к записи сообщества'),
        (POST_USER_MENTION, 'упомянул сообщество в записи'),
        (POST_COMMENT_USER_MENTION, 'упомянул сообщество в комментарии к записи'),
        (LIKE, 'понравилась запись сообщества'),
        (DISLIKE, 'не понравилась запись сообщества'),
        (LIKE_COMMENT, 'понравился комментарий в сообществе'),
        (DISLIKE_COMMENT, 'не понравился комментарий в сообществе'),
        (REPOST, 'поделился записью сообщества'),
    )

    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='video_community_notifications', verbose_name="Сообщество")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_recipient', verbose_name="Получатель")
    timestamp = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    objects = VideoNotificationQS.as_manager()
    video = models.ForeignKey('video.Video', blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('video.VideoComment', blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - ролики сообщества"
        verbose_name_plural = "Уведомления - ролики сообщества"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        if self.video and not self.comment:
            return '{} {} {}'.format(self.actor, self.get_verb_display(), self.video)
        else:
            return '{} {} {} {}'.format(self.actor, self.get_verb_display(), self.comment, self.video)

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def video_notification_handler(actor, recipient, verb, video, comment, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    VideoNotification.objects.create(actor=actor, recipient=recipient, verb=verb, video=video, comment=comment)
    video_notification_broadcast(actor, key, recipient=recipient.username)


def video_community_notification_handler(actor, community, recipient, video, verb, comment, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        VideoCommunityNotification.objects.create(actor=actor, community=community, video=video, comment=comment, recipient=user, verb=verb)
    item_notification_broadcast(actor, key)


def video_notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    recipient = kwargs.pop('recipient', None)
    payload = {'type': 'receive','key': key,'actor_name': actor.get_full_name(),'recipient': recipient}
    async_to_sync(channel_layer.group_send)('notifications', payload)
