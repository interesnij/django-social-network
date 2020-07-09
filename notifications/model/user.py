import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from slugify import slugify
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class UserNotificationQS(models.query.QuerySet):
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


class UserNotification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_notifications', on_delete=models.CASCADE, verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    COMMUNITY_INVITE = 'CI'

    NOTIFICATION_TYPES = (
        (CONNECTION_REQUEST, 'подал заявку в друзья'),
        (CONNECTION_CONFIRMED, 'подтвердил, что он Ваш друг'),
        (COMMUNITY_INVITE, 'пригласил Вас в сообщество'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = UserNotificationQS.as_manager()

    class Meta:
        verbose_name = "Уведомление пользователя"
        verbose_name_plural = "Уведомления пользователя"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


class UserCommunityNotification(models.Model):
    community = models.ForeignKey('communities.Community', related_name='community_users_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='community_user_recipient', on_delete=models.CASCADE, verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    JOIN = 'J'

    NOTIFICATION_TYPES = (
        (CONNECTION_REQUEST, 'подал заявку в сообщество'),
        (CONNECTION_CONFIRMED, 'принят в сообщество'),
        (JOIN, 'вступил в сообщество'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = UserNotificationQS.as_manager()

    class Meta:
        verbose_name = "Уведомление сообщества"
        verbose_name_plural = "Уведомления сообщества"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

def notification_handler(actor, recipient, verb, **kwargs):

    key = kwargs.pop('key', 'notification')
    UserNotification.objects.create(actor=actor, recipient=recipient, verb=verb)
    user_notification_broadcast(actor, key, recipient=recipient.username)

def community_notification_handler(actor, community, recipient, verb, comment, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        UserCommunityNotification.objects.create(actor=actor, community=community, recipient=user, verb=verb)
    user_notification_broadcast(actor, key)


def user_notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    recipient = kwargs.pop('recipient', None)
    payload = {
            'type': 'receive',
            'key': key,
            'actor_name': actor.get_full_name(),
            'recipient': recipient
        }
    async_to_sync(channel_layer.group_send)('notifications', payload)
