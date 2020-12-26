from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from django.utils.formats import localize


class SurveyNotify(models.Model):
    ANON_VOTE = 'AV'
    VOTE = 'V'
    REPOST = 'RE'
    COMMUNITY_REPOST = 'CR'

    NOTIFICATION_TYPES = (
        (ANON_VOTE, 'Аноним принял участие в опросе'),
        (VOTE, ' принял участие в опросе'),

        (REPOST, 'поделился Вашим опросом'),
        (COMMUNITY_REPOST, 'поделилось Вашим опросом'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    survey = models.ForeignKey('survey.Survey', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

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

    def get_svg(self):
        if self.verb == "L" or self.verb == "LC" or self.verb == "LRC":
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/></svg>'
        elif self.verb == "D" or self.verb == "D" or self.verb == "DRC":
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><circle cx="15.5" cy="9.5" r="1.5"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm0-6c-2.33 0-4.32 1.45-5.12 3.5h1.67c.69-1.19 1.97-2 3.45-2s2.75.81 3.45 2h1.67c-.8-2.05-2.79-3.5-5.12-3.5z"/></svg>'
        elif self.verb == "PC" or self.verb == "PCR":
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>'
        elif self.verb == PostNotify.REPOST or self.verb == PostNotify.COMMUNITY_REPOST:
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg>'
        else:
            return ''

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, unread=True).update(unread=False)


class SurveyCommunityNotify(models.Model):
    ANON_VOTE = 'AV'
    VOTE = 'V'
    REPOST = 'RE'
    COMMUNITY_REPOST = 'CR'

    NOTIFICATION_TYPES = (
        (ANON_VOTE, 'Аноним принял участие в опросе'),
        (VOTE, ' принял участие в опросе'),

        (REPOST, 'поделился Вашим опросом'),
        (COMMUNITY_REPOST, 'поделилось Вашим опросом'),
    )

    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='survey_community_notifications', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_survey_recipient', verbose_name="Получатель")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    survey = models.ForeignKey('survey.Survey', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

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
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_svg(self):
        if self.verb == "L" or self.verb == "LC" or self.verb == "LRC":
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/></svg>'
        elif self.verb == "D" or self.verb == "D" or self.verb == "DRC":
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><circle cx="15.5" cy="9.5" r="1.5"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm0-6c-2.33 0-4.32 1.45-5.12 3.5h1.67c.69-1.19 1.97-2 3.45-2s2.75.81 3.45 2h1.67c-.8-2.05-2.79-3.5-5.12-3.5z"/></svg>'
        elif self.verb == "PC" or self.verb == "PCR":
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>'
        elif self.verb == PostCommunityNotify.REPOST or self.verb == PostCommunityNotify.COMMUNITY_REPOST:
            return '<svg fill="currentColor" class="svg_default" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg>'
        else:
            return ''


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
