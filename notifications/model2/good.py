import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from slugify import slugify
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class GoodNotificationQS(models.query.QuerySet):
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


class GoodNotification(models.Model):
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
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    objects =  GoodNotificationQS.as_manager()
    good = models.ForeignKey('goods.Good', blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('goods.GoodComment', blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - товары пользователя"
        verbose_name_plural = "Уведомления - товары пользователя"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} {} {}'.format(self.actor, self.get_verb_display(), self.good)

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


class GoodCommunityNotification(models.Model):
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
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    objects = GoodNotificationQS.as_manager()
    good = models.ForeignKey('goods.Good', blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('goods.GoodComment', blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - товары сообщества"
        verbose_name_plural = "Уведомления - товары сообщества"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} - {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def good_notification_handler(actor, recipient, verb, good, comment, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    PhotoNotification.objects.create(actor=actor, recipient=recipient, verb=verb, good=good, comment=comment)
    photo_notification_broadcast(actor, key, recipient=recipient.username)

def good_community_notification_handler(actor, community, recipient, good, verb, comment, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        PhotoCommunityNotification.objects.create(actor=actor, community=community, good=good, comment=comment, recipient=user, verb=verb)
    item_notification_broadcast(actor, key)


def good_notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    recipient = kwargs.pop('recipient', None)
    payload = {'type': 'receive','key': key,'actor_name': actor.get_full_name(),'recipient': recipient}
    async_to_sync(channel_layer.group_send)('notifications', payload)

    async_to_sync(channel_layer.group_send)('notifications', payload)
