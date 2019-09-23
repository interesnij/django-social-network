from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from users.models import User
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from slugify import slugify
import uuid
from django.core import serializers


class NotificationQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def unread(self):
        """Return only unread items in the current queryset"""
        return self.filter(unread=True)

    def read(self):
        """Return only read items in the current queryset"""
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)

        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read elements in the current queryset with
        optional filter by recipient first.
        """
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



class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="notify_actor",verbose_name="Инициатор",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создано")
    unread  = models.BooleanField(default=True, db_index=True)

    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    FOLLOW = 'F'
    COMMUNITY_INVITE = 'CI'
    POST_USER_MENTION = 'PUM'
    POST_COMMENT_USER_MENTION = 'PCUM'
    LIKED = 'L'
    LIKED_COMMENT =  'LC'
    DISLIKED = 'DL'
    DISLIKED_COMMENT =  'DC'
    LOGGED_IN = 'I'
    LOGGED_OUT = 'O'
    SIGNUP = 'U'
    REPLY = 'R'

    NOTIFICATION_TYPES = (
        (POST_COMMENT, 'Комментарий к посту'),
        (POST_COMMENT_REPLY, 'Ответ на комментарий к посту'),
        (CONNECTION_REQUEST, 'Заявка в друзья'),
        (CONNECTION_CONFIRMED, 'Одобренная заявка в друзья'),
        (FOLLOW, 'Подписка'),
        (COMMUNITY_INVITE, 'Приглашение в сообщество'),
        (POST_USER_MENTION, 'Упоминание пользователя в посте'),
        (POST_COMMENT_USER_MENTION, 'Упоминание пользователя в комментарии к посту'),
        (LIKED, 'Упоминание пользователя о лайке к посту'),
        (LIKED_COMMENT, 'Упоминание пользователя о лайке на комментарий к посту'),
        (DISLIKED, 'Упоминание пользователя о дизлайке к посту'),
        (DISLIKED_COMMENT, 'Упоминание пользователя о дизлайке на комментарий к посту'),
        (SIGNUP, 'Упоминание пользователя о созданном аккаунте'),
        (REPLY, 'Упоминание пользователя о ответе на пост'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES,verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    action_object_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    action_object_object_id = models.CharField(max_length=50, blank=True, null=True)
    action_object = GenericForeignKey("action_object_content_type", "action_object_object_id")
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-timestamp"]

    def __str__(self):
        return '{self.actor} {self.get_verb_display()} {self.time_since()} ago'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('{} {} {}'.format(actor, get_verb_display(), time_since()), to_lower=True, max_length=200)

        super().save(*args, **kwargs)

    def time_since(self, now=None):
        from django.utils.timesince import timesince

        return timesince(self.timestamp, now)

    def get_icon(self):
        if self.verb == 'C' or self.verb == 'A' or self.verb == 'K':
            return 'fa-comment'

        elif self.verb == 'I' or self.verb == 'U' or self.verb == 'O':
            return 'fa-users'

        elif self.verb == 'L':
            return 'fa-heart'

        elif self.verb == 'F':
            return 'fa-star'

        elif self.verb == 'W':
            return 'fa-check-circle'

        elif self.verb == 'E':
            return 'fa-pencil'

        elif self.verb == 'V':
            return 'fa-plus'

        elif self.verb == 'S':
            return 'fa-share-alt'

        elif self.verb == 'R':
            return 'fa-reply'

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notification_handler(actor, recipient, verb, **kwargs):

    key = kwargs.pop('key', 'notification')
    id_value = kwargs.pop('id_value', None)
    if recipient == 'global':
        users = User.objects.all().exclude(username=actor.username)
        for user in users:
            Notification.objects.create(
                actor=actor,
                recipient=user,
                verb=verb,
                action_object=kwargs.pop('action_object', None)
            )
        notification_broadcast(actor, key)

    elif isinstance(recipient, list):
        for user in recipient:
            Notification.objects.create(
                actor=actor,
                recipient=User.objects.get(username=user.username),
                verb=verb,
                action_object=kwargs.pop('action_object', None)
            )

    elif isinstance(recipient, get_user_model()):
        Notification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=kwargs.pop('action_object', None)
        )
        notification_broadcast(
            actor, key, id_value=id_value, recipient=recipient.username)

    else:
        pass


def notification_broadcast(actor, key, **kwargs):
    channel_layer = get_channel_layer()
    id_value = kwargs.pop('id_value', None)
    recipient = kwargs.pop('recipient', None)
    payload = {
            'type': 'receive',
            'key': key,
            'actor_name': actor.get_full_name(),
            'id_value': id_value,
            'recipient': recipient
        }
    async_to_sync(channel_layer.group_send)('notifications', payload)
