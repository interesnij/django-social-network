from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class UserNotify(models.Model):
    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    COMMUNITY_INVITE = 'CI'

    NOTIFICATION_TYPES = (
        (CONNECTION_REQUEST, 'подал заявку в друзья'),
        (CONNECTION_CONFIRMED, 'подтвердил, что он Ваш друг'),
        (COMMUNITY_INVITE, 'пригласил Вас в сообщество'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_notifications', on_delete=models.CASCADE, verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление пользователя"
        verbose_name_plural = "Уведомления пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


class UserCommunityNotify(models.Model):
    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    JOIN = 'J'

    NOTIFICATION_TYPES = (
        (CONNECTION_REQUEST, 'подал заявку в сообщество'),
        (CONNECTION_CONFIRMED, 'принят в сообщество'),
        (JOIN, 'вступил в сообщество'),
    )

    community = models.ForeignKey('communities.Community', related_name='community_users_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='community_user_recipient', on_delete=models.CASCADE, verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление сообщества"
        verbose_name_plural = "Уведомления сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(community_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

def notification_handler(creator, recipient, verb, **kwargs):
    key = kwargs.pop('key', 'notification')
    UserNotify.objects.create(creator=creator, recipient=recipient, verb=verb)
    user_notification_broadcast(key, recipient.pk)

def user_notification_broadcast(key, recipient_pk, **kwargs):
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient_pk,
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def community_notification_handler(creator, community, verb):
    persons = community.get_staff_members()
    for user in persons:
        UserCommunityNotify.objects.create(creator=creator, community=community, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'name': "community_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)
