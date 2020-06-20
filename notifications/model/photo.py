import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from slugify import slugify
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex


class PhotoNotificationQS(models.query.QuerySet):
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


class PhotoNotification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_notifications', verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

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
        (POST_COMMENT, 'оставил комментарий к изображению'),
        (POST_COMMENT_REPLY, 'ответил на Ваш комментарий к изображению'),
        (LIKE, 'понравилось Ваше изображение'),
        (DISLIKE, 'не понравилось Ваше изображение'),
        (LIKE_COMMENT, 'понравился Ваш комментарий к изображению'),
        (DISLIKE_COMMENT, 'не понравился Ваш комментарий к изображению'),
        (LIKE_REPLY_COMMENT, 'понравился Ваш ответ на комментарий к изображению'),
        (DISLIKE_REPLY_COMMENT, 'не понравился Ваш ответ к комментарий к изображению'),
        (REPOST, 'поделился Вашим изображением'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects =  PhotoNotificationQS.as_manager()
    photo = models.ForeignKey('gallery.Photo', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Уведомление - фотографии пользователя"
        verbose_name_plural = "Уведомления - фотографии пользователя"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} - {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


class PhotoCommunityNotification(models.Model):
    community = models.ForeignKey('communities.Community', related_name='community_photo_notify', on_delete=models.CASCADE, verbose_name="Сообщество")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_photo_recipient', verbose_name="Сообщество")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Инициатор", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

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
        (POST_COMMENT, 'оставил комментарий к изображению сообщества'),
        (POST_COMMENT_REPLY, 'ответил на комментарий к изображению сообщества'),
        (LIKE, 'понравилось изображение сообщества'),
        (DISLIKE, 'не понравилось изображение сообщества'),
        (LIKE_COMMENT, 'понравился комментарий к изображению сообщества'),
        (DISLIKE_COMMENT, 'не понравился комментарий к изображению сообщества'),
        (LIKE_REPLY_COMMENT, 'понравился ответ на комментарий к изображению сообщества'),
        (DISLIKE_REPLY_COMMENT, 'не понравился ответ к комментарий к изображению сообщества'),
        (REPOST, 'поделился изображением сообщества'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES, verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = PhotoNotificationQS.as_manager()
    photo = models.ForeignKey('gallery.Photo', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Уведомление - фотографии сообщества"
        verbose_name_plural = "Уведомления - фотографии сообщества"
        ordering = ["-timestamp"]
        indexes = (BrinIndex(fields=['timestamp']),)

    def __str__(self):
        return '{} - {}'.format(self.actor, self.get_verb_display())

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

def photo_notification_handler(actor, recipient, verb, item, comment, **kwargs):
    from users.models import User

    key = kwargs.pop('key', 'notification')
    PhotoNotification.objects.create(actor=actor, recipient=recipient, verb=verb, item=item, comment=comment)
    photo_notification_broadcast(actor, key, recipient=recipient.username)

def photo_community_notification_handler(actor, community, recipient, item, verb, comment, **kwargs):
    key = kwargs.pop('key', 'notification')
    persons = community.get_staff_members()
    for user in persons:
        PhotoCommunityNotification.objects.create(actor=actor, community=community, item=item, comment=comment, recipient=user, verb=verb)
    item_notification_broadcast(actor, key)


def photo_notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    recipient = kwargs.pop('recipient', None)
    payload = {'type': 'receive','key': key,'actor_name': actor.get_full_name(),'recipient': recipient}
    async_to_sync(channel_layer.group_send)('notifications', payload)
