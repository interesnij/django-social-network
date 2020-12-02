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
    COMMUNITY_REPOST = 'CR'
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
        (COMMUNITY_REPOST, 'поделилось Вашей записью'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_notifications', verbose_name="Получатель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    unread  = models.BooleanField(default=True)
    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    post = models.ForeignKey('posts.Post', null=True, blank=True, on_delete=models.CASCADE)
    post_comment = models.ForeignKey('posts.PostComment', blank=True, null=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    community = models.ForeignKey('communities.Community', null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Уведомление - записи пользователя"
        verbose_name_plural = "Уведомления - записи пользователя"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.community:
            return '{} {}'.format(self.community, self.get_verb_display())
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


class PostCommunityNotify(models.Model):
    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    COMMUNITY_INVITE = 'CI'
    POST_USER_MENTION = 'PUM'
    POST_COMMENT_USER_MENTION = 'PCUM'
    REPOST = 'R'
    USER_REPOST = 'UR'
    LIKE = 'L'
    DISLIKE = 'D'
    LIKE_REPLY_COMMENT = 'LRC'
    DISLIKE_REPLY_COMMENT = 'DRC'
    LIKE_COMMENT =  'LC'
    DISLIKE_COMMENT =  'DC'

    NOTIFICATION_TYPES = (
        (POST_COMMENT, 'оставил комментарий к записи'),
        (POST_COMMENT_REPLY, 'ответил на комментарий к записи'),
        (POST_USER_MENTION, 'упомянул сообщество в записи'),
        (POST_COMMENT_USER_MENTION, 'упомянул сообщество в комментарии к записи'),
        (LIKE, 'понравилась запись'),
        (DISLIKE, 'не понравилась запись'),
        (LIKE_COMMENT, 'понравился комментарий'),
        (DISLIKE_COMMENT, 'не понравился комментарий'),
        (REPOST, 'поделился записью'),
        (COMMUNITY_REPOST, 'поделилось записью'),
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
    community_creator = models.ForeignKey('communities.Community', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    class Meta:
        verbose_name = "Уведомление - записи сообщества"
        verbose_name_plural = "Уведомления - записи сообщества"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        if self.community_creator:
            return '{} {}'.format(self.community_creator, self.get_verb_display())
        else:
            return '{} {}'.format(self.creator, self.get_verb_display())

    @classmethod
    def notify_unread(cls, community_pk, user_pk):
        cls.objects.filter(community_id=community_pk, recipient_id=user_pk, unread=True).update(unread=False)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)


def post_notification_handler(creator, recipient, community, post, verb):
    from users.models import User

    PostNotify.objects.create(creator=creator, recipient=recipient, community=community, post=post, verb=verb)
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


def post_community_notification_handler(creator, community, community_creator, post, verb):
    persons = community.get_staff_members()
    for user in persons:
        PostCommunityNotify.objects.create(creator=creator, community=community, community_creator=community_creator, post=post, recipient=user, verb=verb)
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
