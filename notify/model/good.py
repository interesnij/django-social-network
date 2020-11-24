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
        (POST_COMMENT, 'оставил комментарий к товару'),
        (POST_COMMENT_REPLY, 'ответил на Ваш комментарий к товару'),
        (LIKE, 'понравился Ваш товар'),
        (DISLIKE, 'не понравился Ваш товар'),
        (LIKE_COMMENT, 'понравился Ваш комментарий к товару'),
        (DISLIKE_COMMENT, 'не понравился Ваш комментарий к товару'),
        (LIKE_REPLY_COMMENT, 'понравился Ваш ответ на комментарий к товару'),
        (DISLIKE_REPLY_COMMENT, 'не понравился Ваш ответ к комментарий к товару'),
        (REPOST, 'поделился Вашим товаром'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    good = models.ForeignKey('goods.Good', null=True, blank=True, on_delete=models.CASCADE)
    good_comment = models.ForeignKey('goods.GoodComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

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
        (POST_COMMENT, 'оставил комментарий к товару сообщества'),
        (POST_COMMENT_REPLY, 'ответил на комментарий к товару сообщества'),
        (LIKE, 'понравился товар сообщества'),
        (DISLIKE, 'не понравился товар сообщества'),
        (LIKE_COMMENT, 'понравился комментарий к товару сообщества'),
        (DISLIKE_COMMENT, 'не понравился комментарий к товару сообщества'),
        (LIKE_REPLY_COMMENT, 'понравился ответ на комментарий к товару сообщества'),
        (DISLIKE_REPLY_COMMENT, 'не понравился ответ к комментарий к товару сообщества'),
        (REPOST, 'поделился товаром сообщества'),
    )

    community = models.ForeignKey('communities.Community', related_name='community_good_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_good_recipient', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    good = models.ForeignKey('goods.Good', null=True, blank=True, on_delete=models.CASCADE)
    good_comment = models.ForeignKey('goods.GoodComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - товары сообщества"
        verbose_name_plural = "Уведомления - товары сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} - {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(community_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


def good_notification_handler(creator, recipient, good, verb, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    GoodNotify.objects.create(creator=creator, recipient=recipient, good=good, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'good_id': good.pk,
            'object': "good_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def good_comment_notification_handler(creator, recipient, comment, verb, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    GoodNotify.objects.create(creator=creator, recipient=recipient, good_comment=comment, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'comment_id': comment.pk,
            'object': "good_comment_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def good_reply_notification_handler(creator, recipient=recipient, reply, verb, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    GoodNotify.objects.create(creator=creator, recipient=recipient, good_comment=reply, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'reply_id': reply.pk,
            'object': "good_reply_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def good_community_notification_handler(creator, community, good, verb, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        GoodCommunityNotify.objects.create(creator=creator, community=community, good=good, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'good_id': good.pk,
            'object': "community_good_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


def good_comment_community_notification_handler(creator, community, comment, verb, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        GoodCommunityNotify.objects.create(creator=creator, community=community, good_comment=comment, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'comment_id': comment.pk,
            'object': "community_good_comment_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def good_reply_community_notification_handler(creator, community, reply, verb, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        GoodCommunityNotify.objects.create(creator=creator, community=community, good_comment=reply, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'reply_id': reply.pk,
            'object': "community_good_reply_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)
