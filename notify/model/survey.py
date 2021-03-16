from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from django.utils.formats import localize
from notify.helpers import STATUS


class SurveyNotify(models.Model):
    ANON_VOTE = 'AV'
    VOTE = 'V'
    REPOST = 'RE'
    COMMUNITY_REPOST = 'CR'

    VERB = (
        (ANON_VOTE, 'Аноним принял участие в опросе'),
        (VOTE, ' принял участие в опросе'),

        (REPOST, 'поделился'),
        (COMMUNITY_REPOST, 'поделилось'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default=UNREAD, verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    survey = models.ForeignKey('survey.Survey', null=True, blank=True, on_delete=models.CASCADE)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление - опросы пользователя"
        verbose_name_plural = "Уведомления - опросы пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.community:
            return '{} {}'.format(self.community, self.get_verb_display())
        elif self.verb == self.ANON_VOTE:
            return '{}'.format(self.get_verb_display())
        else:
            return '{} {}'.format(self.creator, self.get_verb_display())

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, status=UNREAD).update(status=READ)

    def is_unread(self):
        return self.status is UNREAD


class SurveyCommunityNotify(models.Model):
    ANON_VOTE = 'AV'
    VOTE = 'V'
    REPOST = 'RE'
    COMMUNITY_REPOST = 'CR'

    VERB = (
        (ANON_VOTE, 'Аноним принял участие в опросе'),
        (VOTE, ' принял участие в опросе'),

        (REPOST, 'поделился'),
        (COMMUNITY_REPOST, 'поделилось'),
    )

    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='survey_community_notifications', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_survey_recipient', verbose_name="Получатель")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=1, choices=STATUS, default=UNREAD, verbose_name="Статус")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    survey = models.ForeignKey('survey.Survey', null=True, blank=True, on_delete=models.CASCADE)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление - опросы сообщества"
        verbose_name_plural = "Уведомления - опросы сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.community_creator:
            return '{} {}'.format(self.community_creator, self.get_verb_display())
        elif self.verb == self.ANON_VOTE:
            return '{}'.format(self.get_verb_display())
        else:
            return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, status=UNREAD).update(status=READ)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_unread(self):
        return self.status is UNREAD


def survey_notification_handler(creator, recipient, survey, verb):
    SurveyNotify.objects.create(creator=creator, recipient=recipient, survey=survey, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'survey_id': str(survey.pk),
            'name': "u_survey_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def survey_repost_notification_handler(creator, recipient, community, survey, verb):
    SurveyNotify.objects.create(creator=creator, recipient=recipient, community=community, survey=survey, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'survey_id': str(survey.pk),
            'name': "u_survey_repost_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def survey_community_notification_handler(creator, community, survey, verb):
    persons = community.get_staff_members()
    for user in persons:
        if creator.pk != user.pk:
            SurveyCommunityNotify.objects.create(creator=creator, community=community, survey=survey, recipient=user, verb=verb)
            channel_layer = get_channel_layer()
            payload = {
                'type': 'receive',
                'key': 'notification',
                'recipient_id': user.pk,
                'community_id': community.pk,
                'survey_id':  str(survey.pk),
                'name': "c_survey_notify",
            }
            async_to_sync(channel_layer.group_send)('notification', payload)

def survey_repost_community_notification_handler(creator, community, community_creator, survey, verb):
    persons = community.get_staff_members()
    for user in persons:
        if creator.pk != user.pk:
            SurveyCommunityNotify.objects.create(creator=creator, community=community, community_creator=community_creator, survey=survey, recipient=user, verb=verb)
            channel_layer = get_channel_layer()
            payload = {
                'type': 'receive',
                'key': 'notification',
                'recipient_id': user.pk,
                'community_id': community.pk,
                'survey_id':  str(survey.pk),
                'name': "c_survey_repost_notify",
            }
            async_to_sync(channel_layer.group_send)('notification', payload)
