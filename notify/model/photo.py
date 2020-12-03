from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class PhotoNotify(models.Model):
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
        (COMMENT, 'оставил комментарий к фото'),
        (REPLY, 'ответил на Ваш комментарий к фото'),
        (USER_MENTION, 'упомянул Вас в фото'),
        (COMMENT_USER_MENTION, 'упомянул Вас в комментарии к фото'),
        (LIKE, 'оценил Ваше фото'),
        (DISLIKE, 'не оценил Ваше фото'),
        (LIKE_COMMENT, 'оценил Ваш комментарий к фото'),
        (DISLIKE_COMMENT, 'не оценил Ваш комментарий к фото'),
        (LIKE_REPLY, 'оценил Ваш ответ на комментарий к фото'),
        (DISLIKE_REPLY, 'не оценил Ваш ответ к комментарий к фото'),

        (REPOST, 'поделился Вашей фотографией'),
        (COMMUNITY_REPOST, 'поделилось Вашей фотографией'),
        (ALBUM_REPOST, 'поделился Вашим фотоальбомом'),
        (ALBUM_COMMUNITY_REPOST, 'поделилось Вашим фотоальбомом'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    photo = models.ForeignKey('gallery.Photo', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('gallery.Album', null=True, blank=True, on_delete=models.CASCADE)
    photo_comment = models.ForeignKey('gallery.PhotoComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

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
    COMMENT = 'C'
    REPLY = 'R'
    USER_MENTION = 'UM'
    COMMENT_USER_MENTION = 'CUM'
    LIKE = 'L'
    DISLIKE = 'D'
    LIKE_REPLY = 'LRC'
    DISLIKE_REPLY = 'DRC'
    LIKE_COMMENT =  'LC'
    DISLIKE_COMMENT =  'DC'

    REPOST = 'RE'
    ALBUM_REPOST = 'ARE'
    COMMUNITY_REPOST = 'CR'
    ALBUM_COMMUNITY_REPOST = 'ACR'

    NOTIFICATION_TYPES = (
        (COMMENT, 'оставил комментарий к изображению сообщества'),
        (REPLY, 'ответил на комментарий к изображению сообщества'),
        (LIKE, 'понравилось изображение сообщества'),
        (DISLIKE, 'не понравилось изображение сообщества'),
        (LIKE_COMMENT, 'понравился комментарий к изображению сообщества'),
        (DISLIKE_COMMENT, 'не понравился комментарий к изображению сообщества'),
        (LIKE_REPLY, 'понравился ответ на комментарий к изображению сообщества'),
        (DISLIKE_REPLY, 'не понравился ответ к комментарий к изображению сообщества'),

        (REPOST, 'поделился фотографией'),
        (COMMUNITY_REPOST, 'поделилось фотографией'),
        (ALBUM_REPOST, 'поделился фотоальбомом'),
        (ALBUM_COMMUNITY_REPOST, 'поделилось фотоальбомом'),
    )

    community = models.ForeignKey('communities.Community', related_name='community_photo_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_photo_recipient', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    photo = models.ForeignKey('gallery.Photo', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('gallery.Album', null=True, blank=True, on_delete=models.CASCADE)
    photo_comment = models.ForeignKey('gallery.PhotoComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

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


def photo_notification_handler(creator, recipient, community, photo, album, verb):
    PhotoNotify.objects.create(creator=creator, recipient=recipient, community=community, photo=photo, album=album, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'photo_id': photo.pk,
            'name': "u_photo_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def photo_comment_notification_handler(creator, recipient, comment, verb):
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


def photo_community_notification_handler(creator, community, community_creator, photo, album, verb):
    persons = community.get_staff_members()
    for user in persons:
        if creator.pk != user.pk:
            PhotoCommunityNotify.objects.create(
                                                creator=creator,
                                                community=community,
                                                community_creator=community_creator,
                                                photo=photo,
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
                'photo_id': photo.pk,
                'name': "c_photo_notify",
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
