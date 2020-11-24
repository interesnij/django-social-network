from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class PostNotify(models.Model):
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

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    post = models.ForeignKey('posts.Post', null=True, blank=True, on_delete=models.CASCADE)
    post_comment = models.ForeignKey('posts.PostComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - записи пользователя"
        verbose_name_plural = "Уведомления - записи пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return '{} {}'.format(self.creator, self.get_verb_display())

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, unread=True).update(unread=False)


class PostCommunityNotify(models.Model):
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
        (REPOST, 'поделился записью сообщества'),
    )

    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='post_community_notifications', verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_post_recipient', verbose_name="Получатель")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    post = models.ForeignKey('posts.Post', null=True, blank=True, on_delete=models.CASCADE)
    post_comment = models.ForeignKey('posts.PostComment', null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = "Уведомление - записи сообщества"
        verbose_name_plural = "Уведомления - записи сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.post and not self.comment:
            return '{} {}'.format(self.creator, self.get_verb_display(), self.post)
        else:
            return '{} {} {}'.format(self.creator, self.get_verb_display(), self.comment, self.post)

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(community_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


def post_notification_handler(creator, recipient, verb, post, comment, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    PostNotify.objects.create(creator=creator, recipient=recipient, verb=verb, post=post, comment=comment)
    post_notification_broadcast(creator, key, recipient=recipient.username)


def post_community_notification_handler(creator, community, recipient, post, verb, comment, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        PostCommunityNotify.objects.create(actor=actor, community=community, post=post, comment=comment, recipient=user, verb=verb)
    post_notification_broadcast(actor, key)


def post_notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    recipient = kwargs.pop('recipient', None)
    payload = {'type': 'receive','key': key,'actor_name': actor.get_full_name(),'recipient': recipient}
    async_to_sync(channel_layer.group_send)('notifications', payload)
