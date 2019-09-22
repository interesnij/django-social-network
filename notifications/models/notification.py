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
        """Mark as read any unread elements in the current queryset with
        optional filter by recipient first.
        """
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
        """Returns a serialized version of the most recent unread elements in
        the queryset"""
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]

        notification_dic = serializers.serialize("json", qs)
        return notification_dic

    def get_most_recent(self, recipient=None):
        """Returns the most recent unread elements in the queryset"""
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]

        return qs



class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',verbose_name="Получатель")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="notify_actor",verbose_name="Инициатор",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создано")
    unread  = models.BooleanField(default=False,verbose_name="Прочитано")

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
            self.slug = slugify('{self.recipient} {self.uuid_id} {self.verb}',
                                max_length=200)

        super().save(*args, **kwargs)

    def time_since(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince

        return timesince(self.timestamp, now)

    def get_icon(self):
        """Model method to validate notification type and return the closest
        icon to the verb.
        """
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
    """
    Функция обработчика для создания экземпляра уведомления.
    :требует:
    : param actor: пользовательский экземпляр того пользователя, который выполняет действие.
    : param recipient: экземпляр пользователя, список экземпляров пользователя или строка
                      "глобальный", определяющий, кто должен быть уведомлен.
    : param verb: атрибут уведомления с правильным выбором из списка.
    :Факультативный:
    : param action_object: экземпляр модели, на котором была выполнена команда.
    :param key: строка, определяющая, какое уведомление будет создано.
    : param id_value: значение UUID, присвоенное определенному элементу в DOM.
    """
    key = kwargs.pop('key', 'notification')
    id_value = kwargs.pop('id_value', None)
    if recipient == 'global':
        users = User.objects.all().exclude(id=actor.id)
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
                recipient=User.objects.get(id=user),
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
            actor, key, id_value=id_value, recipient=recipient.det_full_name)

    else:
        pass


def notification_broadcast(actor, key, **kwargs):
    """Обработчик уведомлений для широковещательных вызовов на уровень recieve
    WebSocket потребитель этого приложения.
    :требует:
    : param actor: пользовательский экземпляр того пользователя, который выполняет действие.
    : param key: Строковый параметр, указывающий клиенту, какое действие
                выполнять.
    :Факультативный:
    : param id_value: значение UUID, присвоенное определенному элементу в DOM.
    :парам получателя: строка, указывающая имя того, кто должен быть
                      предупрежденный.
    """
    channel_layer = get_channel_layer()
    id_value = kwargs.pop('id_value', None)
    recipient = kwargs.pop('recipient', None)
    payload = {
            'type': 'receive',
            'key': key,
            'actor_name': actor.id,
            'id_value': id_value,
            'recipient': recipient
        }
    async_to_sync(channel_layer.group_send)('notifications', payload)
