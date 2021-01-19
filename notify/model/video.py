import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class VideoNotify(models.Model):
    COMMENT = 'C'
    REPLY = 'R'
    USER_MENTION = 'PUM'
    COMMENT_USER_MENTION = 'PCUM'
    LIKE = 'L'
    DISLIKE = 'D'
    LIKE_REPLY = 'LR'
    DISLIKE_REPLY = 'DR'
    LIKE_COMMENT =  'LC'
    DISLIKE_COMMENT =  'DC'

    REPOST = 'RE'
    ALBUM_REPOST = 'ARE'
    COMMUNITY_REPOST = 'CR'
    ALBUM_COMMUNITY_REPOST = 'ACR'

    NOTIFICATION_TYPES = (
        (COMMENT, 'оставил комментарий к видеозаписи'),
        (REPLY, 'ответил на Ваш комментарий к видеозаписи'),
        (USER_MENTION, 'упомянул Вас в видеозаписи'),
        (COMMENT_USER_MENTION, 'упомянул Вас в комментарии к видеозаписи'),
        (LIKE, 'оценил Вашу видеозапись'),
        (DISLIKE, 'не оценил Вашу видеозапись'),
        (LIKE_COMMENT, 'оценил Ваш комментарий к видеозаписи'),
        (DISLIKE_COMMENT, 'не оценил Ваш комментарий к видеозаписи'),
        (LIKE_REPLY, 'оценил Ваш ответ на комментарий к видеозаписи'),
        (DISLIKE_REPLY, 'не оценил Ваш ответ к комментарий к видеозаписи'),

        (REPOST, 'поделился Вашей видеозаписью'),
        (COMMUNITY_REPOST, 'поделилось Вашей видеозаписью'),
        (ALBUM_REPOST, 'поделился Вашим видеоальбомом'),
        (ALBUM_COMMUNITY_REPOST, 'поделилось Вашим видеоальбомом'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('video.VideoAlbum', null=True, blank=True, on_delete=models.CASCADE)
    video_comment = models.ForeignKey('video.VideoComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
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
    COMMENT = 'C'
    REPLY = 'R'
    USER_MENTION = 'UM'
    COMMENT_USER_MENTION = 'CUM'
    LIKE = 'L'
    DISLIKE = 'D'
    LIKE_REPLY = 'LR'
    DISLIKE_REPLY = 'DR'
    LIKE_COMMENT =  'LC'
    DISLIKE_COMMENT =  'DC'

    REPOST = 'RE'
    ALBUM_REPOST = 'ARE'
    COMMUNITY_REPOST = 'CR'
    ALBUM_COMMUNITY_REPOST = 'ACR'

    NOTIFICATION_TYPES = (
        (COMMENT, 'написал комментарий к видеозаписи'),
        (REPLY, 'ответил на комментарий к видеозаписи'),
        (USER_MENTION, 'упомянул сообщество в видеозаписи'),
        (COMMENT_USER_MENTION, 'упомянул сообщество в комментарии к видеозаписи'),
        (LIKE, 'оценил видеозапись'),
        (DISLIKE, 'не оценил видеозапись'),
        (LIKE_COMMENT, 'оценил комментарий к видеозаписи'),
        (DISLIKE_COMMENT, 'не оценил комментарий к видеозаписи'),
        (LIKE_REPLY, 'оценил Ваш ответ на комментарий к видеозаписи'),
        (DISLIKE_REPLY, 'не оценил Ваш ответ к комментарий к видеозаписи'),

        (REPOST, 'поделился видеозаписью'),
        (COMMUNITY_REPOST, 'поделилось видеозаписью'),
        (ALBUM_REPOST, 'поделился фотоальбомом'),
        (ALBUM_COMMUNITY_REPOST, 'поделилось фотоальбомом'),
    )

    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='video_community_notifications', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_recipient', verbose_name="Получатель")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    video = models.ForeignKey('video.Video', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('video.VideoAlbum', null=True, blank=True, on_delete=models.CASCADE)
    video_comment = models.ForeignKey('video.VideoComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
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


def video_notification_handler(creator, recipient, community, video, album, verb):
    VideoNotify.objects.create(creator=creator, recipient=recipient, community=community, video=video, album=album, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'video_id': video.pk,
            'name': "u_video_notify",
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


def video_community_notification_handler(creator, community, community_creator, video, album, verb):
    persons = community.get_staff_members()
    for user in persons:
        if creator.pk != user.pk:
            VideoCommunityNotify.objects.create(
                                                creator=creator,
                                                community=community,
                                                community_creator=community_creator,
                                                video=video,
                                                album=album,
                                                recipient=user,
                                                verb=verb
                                                )
            channel_layer = get_channel_layer()
            payload = {
                'type': 'receive',
                'key': 'notification',
                'recipient_id': user.pk,
                'community_id': community.pk,
                'video_id': video.pk,
                'name': "c_video_notify",
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
