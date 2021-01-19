import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.text import slugify
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class GoodNotify(models.Model):
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
        (COMMENT, 'оставил комментарий к товару'),
        (REPLY, 'ответил на Ваш комментарий к товару'),
        (USER_MENTION, 'упомянул Вас в товаре'),
        (COMMENT_USER_MENTION, 'упомянул Вас в комментарии к товару'),
        (LIKE, 'оценил Вашу товар'),
        (DISLIKE, 'не оценил Вашу товар'),
        (LIKE_COMMENT, 'оценил Ваш комментарий к товару'),
        (DISLIKE_COMMENT, 'не оценил Ваш комментарий к товару'),
        (LIKE_REPLY, 'оценил Ваш ответ на комментарий к товару'),
        (DISLIKE_REPLY, 'не оценил Ваш ответ к комментарий к товару'),

        (REPOST, 'поделился товаром'),
        (COMMUNITY_REPOST, 'поделилось товаром'),
        (ALBUM_REPOST, 'поделился подборкой товаров'),
        (ALBUM_COMMUNITY_REPOST, 'поделилось подборкой товаров'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    good = models.ForeignKey('goods.Good', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('goods.GoodAlbum', null=True, blank=True, on_delete=models.CASCADE)
    good_comment = models.ForeignKey('goods.GoodComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Уведомление - товары пользователя"
        verbose_name_plural = "Уведомления - товары пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {} {}'.format(self.creator, self.get_verb_display(), self.good)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, unread=True).update(unread=False)


class GoodCommunityNotify(models.Model):
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
        (COMMENT, 'написал комментарий к товару'),
        (REPLY, 'ответил на комментарий к товару'),
        (USER_MENTION, 'упомянул сообщество в товаре'),
        (COMMENT_USER_MENTION, 'упомянул сообщество в комментарии к товару'),
        (LIKE, 'оценил товар'),
        (DISLIKE, 'не оценил товар'),
        (LIKE_COMMENT, 'оценил комментарий к товару'),
        (DISLIKE_COMMENT, 'не оценил комментарий к товару'),
        (LIKE_REPLY, 'оценил Ваш ответ на комментарий к товару'),
        (DISLIKE_REPLY, 'не оценил Ваш ответ к комментарий к товару'),

        (REPOST, 'поделился товаром'),
        (COMMUNITY_REPOST, 'поделилось товаром'),
        (ALBUM_REPOST, 'поделился подборкой товаров'),
        (ALBUM_COMMUNITY_REPOST, 'поделилось подборкой товаров'),
    )

    community = models.ForeignKey('communities.Community', related_name='community_good_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_good_recipient', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    good = models.ForeignKey('goods.Good', null=True, blank=True, on_delete=models.CASCADE)
    album = models.ForeignKey('goods.GoodAlbum', null=True, blank=True, on_delete=models.CASCADE)
    good_comment = models.ForeignKey('goods.GoodComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Уведомление - товары сообщества"
        verbose_name_plural = "Уведомления - товары сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} - {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


def good_notification_handler(creator, recipient, community, good, album, verb):
    GoodNotify.objects.create(creator=creator, recipient=recipient, community=community, good=good, album=album, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'good_id': good.pk,
            'name': "u_good_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def good_comment_notification_handler(creator, recipient, comment, verb):
    from users.models import User

    GoodNotify.objects.create(creator=creator, recipient=recipient, good_comment=comment, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'comment_id': comment.pk,
            'name': "good_comment_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def good_reply_notification_handler(creator, recipient, reply, verb):
    from users.models import User

    GoodNotify.objects.create(creator=creator, recipient=recipient, good_comment=reply, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'reply_id': reply.pk,
            'name': "good_reply_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def good_community_notification_handler(creator, community, community_creator, good, album, verb):
    persons = community.get_staff_members()
    for user in persons:
        if creator.pk != user.pk:
            GoodCommunityNotify.objects.create(
                                                creator=creator,
                                                community=community,
                                                community_creator=community_creator,
                                                good=good,
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
                'good_id': good.pk,
                'name': "c_good_notify",
            }
            async_to_sync(channel_layer.group_send)('notification', payload)


def good_comment_community_notification_handler(creator, community, comment, verb):
    persons = community.get_staff_members()
    for user in persons:
        GoodCommunityNotify.objects.create(creator=creator, community=community, good_comment=comment, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'comment_id': comment.pk,
            'name': "community_good_comment_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def good_reply_community_notification_handler(creator, community, reply, verb):
    persons = community.get_staff_members()
    for user in persons:
        GoodCommunityNotify.objects.create(creator=creator, community=community, good_comment=reply, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'reply_id': reply.pk,
            'name': "community_good_reply_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)
