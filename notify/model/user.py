from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from notify.helpers import STATUS


class UserNotify(models.Model):
    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    COMMUNITY_INVITE = 'CI'

    VERB = (
        (CONNECTION_REQUEST, 'подал заявку в друзья'),
        (CONNECTION_CONFIRMED, 'подтвердил, что он Ваш друг'),
        (COMMUNITY_INVITE, 'пригласил Вас в сообщество'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_notifications', on_delete=models.CASCADE, verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление пользователя"
        verbose_name_plural = "Уведомления пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, status=UNREAD).update(status=READ)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_unread(self):
        return self.status is UNREAD


class UserCommunityNotify(models.Model):
    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    JOIN = 'J'

    VERB = (
        (CONNECTION_REQUEST, 'подал заявку в сообщество'),
        (CONNECTION_CONFIRMED, 'принят в сообщество'),
        (JOIN, 'вступил в сообщество'),
    )

    community = models.ForeignKey('communities.Community', related_name='community_users_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='community_user_recipient', on_delete=models.CASCADE, verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление сообщества"
        verbose_name_plural = "Уведомления сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, status=UNREAD).update(status=READ)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_unread(self):
        return self.status is UNREAD

def notification_handler(creator, recipient, verb):
    UserNotify.objects.create(creator=creator, recipient=recipient, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'name': "user_notify",
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
