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
        if self.post and not self.post_comment:
            return '{} {}'.format(self.creator, self.get_verb_display(), self.post)
        else:
            return '{} {} {}'.format(self.creator, self.get_verb_display(), self.post_comment, self.post)

    @classmethod
    def notify_unread(cls, user_pk):
        cls.objects.filter(community_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


def post_notification_handler(creator, recipient, post, verb):
    from users.models import User

    PostNotify.objects.create(creator=creator, recipient=recipient, post=post, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'post_id': str(post.uuid),
            'name': "u_post_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def post_comment_notification_handler(creator, recipient, comment, verb):
    from users.models import User

    PostNotify.objects.create(creator=creator, recipient=recipient, post_comment=comment, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'comment_id': comment.pk,
            'name': "u_post_comment_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def post_reply_notification_handler(creator, recipient, reply, verb):
    from users.models import User

    PostNotify.objects.create(creator=creator, recipient=recipient, post_comment=reply, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': key,
            'recipient_id': recipient.pk,
            'reply_id': reply.pk,
            'name': "u_post_reply_notify",
        }
    async_to_sync(channel_layer.group_send)('notification', payload)


def post_community_notification_handler(creator, community, post, verb):
    persons = community.get_staff_members()
    for user in persons:
        PostCommunityNotify.objects.create(creator=creator, community=community, post=post, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': user.pk,
            'community_id': community.pk,
            'post_id': post.pk,
            'name': "c_post_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


def post_comment_community_notification_handler(creator, community, comment, verb):
    persons = community.get_staff_members()
    for user in persons:
        PostCommunityNotify.objects.create(creator=creator, community=community, post_comment=comment, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'comment_id': comment.pk,
            'name': "c_post_comment_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def post_reply_community_notification_handler(creator, community, reply, verb):
    persons = community.get_staff_members()
    for user in persons:
        PostCommunityNotify.objects.create(creator=creator, community=community, post_comment=reply, recipient=user, verb=verb)
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient.pk,
            'community_id': community.pk,
            'reply_id': reply.pk,
            'name': "c_post_reply_notify",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)
