import uuid
from common.model_loaders import get_user_model, get_community_model
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from slugify import slugify
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class ItemNotificationQS(models.query.QuerySet):
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


class ItemNotification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='item_notifications', verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

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
        (POST_COMMENT, 'оставил комментарий к записи'),
        (POST_COMMENT_REPLY, 'ответил на Ваш комментарий к записи'),
        (POST_USER_MENTION, 'упомянул Вас в записи'),
        (POST_COMMENT_USER_MENTION, 'упомянул Вас в комментарии к записи'),
        (LIKE, 'понравилась Ваша запись'),
        (DISLIKE, 'не понравилась Ваша запись'),
        (LIKE_COMMENT, 'понравился Ваш комментарий к записи'),
        (DISLIKE_COMMENT, 'не понравился Ваш комментарий к записи'),
        (LIKE_REPLY_COMMENT, 'понравился Ваш ответ на комментарий  к записи'),
        (DISLIKE_REPLY_COMMENT, 'не понравился Ваш ответ к комментарий к записи'),
        (REPOST, 'поделился Вашей записью'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects =  ItemNotificationQS.as_manager()

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} - {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


class ItemCommunityNotification(models.Model):
    recipient = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='item_community_notifications', verbose_name="Сообщество")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

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
        (LIKE_REPLY_COMMENT, 'понравился ответ на комментарий в сообществе'),
        (DISLIKE_REPLY_COMMENT, 'не понравился ответ к комментарий в сообществе'),
        (REPOST, 'поделился записью сообщества'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = ItemNotificationQS.as_manager()

    class Meta:
        verbose_name = "Уведомление сообщества"
        verbose_name_plural = "Уведомления сообщества"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} - {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def item_notification_handler(actor, recipient, verb, **kwargs):
    key = kwargs.pop('key', 'notification')

    if recipient == 'global':
        users = User.objects.all().exclude(username=actor.username)
        for user in users:
            UserNotification.objects.create(
                actor=actor,
                recipient=user,
                verb=verb,
            )
        item_notification_broadcast(actor, key)

    elif isinstance(recipient, list):
        for user in recipient:
            UserNotification.objects.create(
                actor=actor,
                recipient=User.objects.get(username=user.username),
                verb=verb,
            )

    elif isinstance(recipient, get_user_model()):
        UserNotification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
        )
        item_notification_broadcast(
            actor, key, recipient=recipient.username)

    else:
        pass


def item_community_notification_handler(actor, recipient, verb, **kwargs):
    key = kwargs.pop('key', 'notification')

    if recipient == 'global':
        users = User.objects.all().exclude(username=actor.username)
        for user in users:
            UserCommunityNotification.objects.create(
                actor=actor,
                recipient=user,
                verb=verb,
            )
        item_notification_broadcast(actor, key)

    elif isinstance(recipient, list):
        for community in recipient:
            UserCommunityNotification.objects.create(
                actor=actor,
                recipient=Community.objects.get(name=community.name),
                verb=verb,
            )

    elif isinstance(recipient, get_community_model()):
        UserCommunityNotification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
        )
        item_notification_broadcast(
            actor, key, recipient=recipient.name)

    else:
        pass


def item_notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    recipient = kwargs.pop('recipient', None)
    payload = {
            'type': 'receive',
            'key': key,
            'actor_name': actor.get_full_name(),
            'recipient': recipient
        }
    async_to_sync(channel_layer.group_send)('notifications', payload)
