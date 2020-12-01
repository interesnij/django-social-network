import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class VideoNotify(models.Model):
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
        (LIKE, 'оценил Ваш ролик'),
        (DISLIKE, 'не оценил Ваш ролик'),
        (LIKE_COMMENT, 'оценил Ваш комментарий к ролику'),
        (DISLIKE_COMMENT, 'не оценил Ваш комментарий к ролику'),
        (LIKE_REPLY_COMMENT, 'оценил Ваш ответ на комментарий  к ролику'),
        (DISLIKE_REPLY_COMMENT, 'не оценил Ваш ответ к комментарий к ролику'),
        (REPOST, 'поделился Вашим роликом'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    video_comment = models.ForeignKey('video.VideoComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

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
    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    COMMUNITY_INVITE = 'CI'
    POST_USER_MENTION = 'PUM'
    POST_COMMENT_USER_MENTION = 'PCUM'
    REPOST = 'R'
    USER_REPOST = 'UR'
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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_recipient', verbose_name="Получатель")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    video_comment = models.ForeignKey('video.VideoComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

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


def video_notification_handler(creator, recipient, video, verb):
    from users.models import User

    VideoNotify.objects.create(creator=creator, recipient=recipient, video=video, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'video_id': video.pk,
            'name': "video_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def video_comment_notification_handler(creator, recipient, comment, verb):
    from users.models import User

    VideoNotify.objects.create(creator=creator, recipient=recipient, video_comment=comment, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'comment_id': comment.pk,
            'name': "video_comment_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def video_reply_notification_handler(creator, recipient, reply, verb):
    from users.models import User

    VideoNotify.objects.create(creator=creator, recipient=recipient, video_comment=reply, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'reply_id': reply.pk,
            'name': "video_reply_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def video_community_notification_handler(creator, community, video, verb):
    persons = community.get_staff_members()
    for user in persons:
        VideoCommunityNotify.objects.create(creator=creator, community=community, video=video, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'video_id': video.pk,
            'name': "community_video_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


def video_comment_community_notification_handler(creator, community, comment, verb):
    persons = community.get_staff_members()
    for user in persons:
        VideoCommunityNotify.objects.create(creator=creator, community=community, video_comment=comment, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'comment_id': comment.pk,
            'name': "community_video_comment_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def video_reply_community_notification_handler(creator, community, reply, verb):
    persons = community.get_staff_members()
    for user in persons:
        VideoCommunityNotify.objects.create(creator=creator, community=community, video_comment=reply, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'reply_id': reply.pk,
            'name': "community_video_reply_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)
