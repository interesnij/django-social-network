from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from notify.helpers import STATUS


class UserNotify(models.Model):
    CONNECTION_REQUEST, WOMAN_CONNECTION_REQUEST, GROUP_CONNECTION_REQUEST = 'CR', 'WCR', 'GCR'
    CONNECTION_CONFIRMED, WOMAN_CONNECTION_CONFIRMED, GROUP_CONNECTION_CONFIRMED = 'CC', 'WCC', 'GCC'
    COMMUNITY_INVITE, WOMAN_COMMUNITY_INVITE, GROUP_COMMUNITY_INVITE = 'CI', 'WCI', 'GCI'
    REGISTER, WOMAN_REGISTER, GROUP_REGISTER = 'R', 'WR', 'GR'
    COMMUNITY_REQUEST_CONFIRMED, GROUP_COMMUNITY_REQUEST_CONFIRMED = 'CRC', 'GCRC'

    VERB = (
        (CONNECTION_REQUEST, 'подал заявку в друзья'), (WOMAN_CONNECTION_REQUEST, 'подала заявку в друзья'), (GROUP_CONNECTION_REQUEST, 'подали заявку в друзья'),
        (CONNECTION_CONFIRMED, 'подтвердил, что он Ваш друг'), (WOMAN_CONNECTION_CONFIRMED, 'подтвердила, что он Ваш друг'), (GROUP_CONNECTION_CONFIRMED, 'подтвердили, что он Ваш друг'),
        (COMMUNITY_INVITE, 'пригласил Вас в сообщество'), (WOMAN_COMMUNITY_INVITE, 'пригласила Вас в сообщество'), (GROUP_COMMUNITY_INVITE, 'пригласили Вас в сообщество'),
        (REGISTER, 'зарегистрировался'), (WOMAN_REGISTER, 'зарегистрировалась'), (GROUP_REGISTER, 'зарегистрировались'),
        (COMMUNITY_REQUEST_CONFIRMED, 'Вы приняты'), (GROUP_COMMUNITY_REQUEST_CONFIRMED, 'Вы приняты'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_notifications', on_delete=models.CASCADE, verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    community = models.ForeignKey('communities.Community', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Сообщество")
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
    CONNECTION_REQUEST, WOMAN_CONNECTION_REQUEST, GROUP_CONNECTION_REQUEST = 'CR', 'WCR', 'GCR'
    CONNECTION_CONFIRMED = 'CC'
    JOIN, WOMAN_JOIN, GROUP_JOIN = 'J', 'WJ', 'GJ'

    VERB = (
        (CONNECTION_REQUEST, 'подал заявку в сообщество'), (WOMAN_CONNECTION_REQUEST, 'подала заявку в сообщество'), (GROUP_CONNECTION_REQUEST, 'подали заявку в сообщество'),
        (CONNECTION_CONFIRMED, 'приняты в сообщество'),
        (JOIN, 'вступил в сообщество'), (WOMAN_JOIN, 'вступила в сообщество'), (GROUP_JOIN, 'вступили в сообщество'),
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
