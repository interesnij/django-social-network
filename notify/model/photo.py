from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class PhotoNotify(models.Model):
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
        (POST_COMMENT, 'оставил комментарий к изображению'),
        (POST_COMMENT_REPLY, 'ответил на Ваш комментарий к изображению'),
        (LIKE, 'оценил Ваше фото'),
        (DISLIKE, 'не оценил Ваше фото'),
        (LIKE_COMMENT, 'оценил Ваш комментарий к фото'),
        (DISLIKE_COMMENT, 'не оценил Ваш комментарий к фото'),
        (LIKE_REPLY_COMMENT, 'оценил Ваш ответ на комментарий к фото'),
        (DISLIKE_REPLY_COMMENT, 'не оценил Ваш ответ к комментарий к фото'),
        (REPOST, 'поделился Вашим фото'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    photo = models.ForeignKey('gallery.Photo', null=True, blank=True, on_delete=models.CASCADE)
    photo_comment = models.ForeignKey('gallery.PhotoComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

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

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, unread=True).update(unread=False)


class PhotoCommunityNotify(models.Model):
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
        (POST_COMMENT, 'оставил комментарий к изображению сообщества'),
        (POST_COMMENT_REPLY, 'ответил на комментарий к изображению сообщества'),
        (LIKE, 'понравилось изображение сообщества'),
        (DISLIKE, 'не понравилось изображение сообщества'),
        (LIKE_COMMENT, 'понравился комментарий к изображению сообщества'),
        (DISLIKE_COMMENT, 'не понравился комментарий к изображению сообщества'),
        (LIKE_REPLY_COMMENT, 'понравился ответ на комментарий к изображению сообщества'),
        (DISLIKE_REPLY_COMMENT, 'не понравился ответ к комментарий к изображению сообщества'),
        (REPOST, 'поделился изображением сообщества'),
    )

    community = models.ForeignKey('communities.Community', related_name='community_photo_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_photo_recipient', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    photo = models.ForeignKey('gallery.Photo', null=True, blank=True, on_delete=models.CASCADE)
    photo_comment = models.ForeignKey('gallery.PhotoComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - фотографии сообщества"
        verbose_name_plural = "Уведомления - фотографии сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


def photo_notification_handler(creator, recipient, photo, verb):
    from users.models import User

    PhotoNotify.objects.create(creator=creator, recipient=recipient, photo=photo, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'photo_id': photo.pk,
            'name': "photo_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def photo_comment_notification_handler(creator, recipient, comment, verb):
    from users.models import User

    PhotoNotify.objects.create(creator=creator, recipient=recipient, photo_comment=comment, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'comment_id': comment.pk,
            'name': "photo_comment_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def photo_reply_notification_handler(creator, recipient, reply, verb):
    from users.models import User

    PhotoNotify.objects.create(creator=creator, recipient=recipient, photo_comment=reply, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'reply_id': reply.pk,
            'name': "photo_reply_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def photo_community_notification_handler(creator, community, photo, verb):
    persons = community.get_staff_members()
    for user in persons:
        PhotoCommunityNotify.objects.create(creator=creator, community=community, photo=photo, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'photo_id': photo.pk,
            'name': "community_photo_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


def photo_comment_community_notification_handler(creator, community, comment, verb):

    persons = community.get_staff_members()
    for user in persons:
        PhotoCommunityNotify.objects.create(creator=creator, community=community, photo_comment=comment, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'comment_id': comment.pk,
            'name': "community_photo_comment_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def photo_reply_community_notification_handler(creator, community, reply, verb):
    persons = community.get_staff_members()
    for user in persons:
        PhotoCommunityNotify.objects.create(creator=creator, community=community, photo_comment=reply, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'reply_id': reply.pk,
            'name': "community_photo_reply_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)
