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
        (LIKE, 'оценил Вашу запись'),
        (DISLIKE, 'не оценил Вашу запись'),
        (LIKE_COMMENT, 'оценил Ваш комментарий к записи'),
        (DISLIKE_COMMENT, 'не оценил Ваш комментарий к записи'),
        (LIKE_REPLY_COMMENT, 'оценил Ваш ответ на комментарий  к записи'),
        (DISLIKE_REPLY_COMMENT, 'не оценил Ваш ответ к комментарий к записи'),
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

    def get_svg(self):
        if self.verb == "L" or self.verb == "LC" or self.verb == "LRC":
            return '<svg fill="#00FF7F" style="position:absolute;width:25px" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/></svg>'

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
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, unread=True).update(unread=False)

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
