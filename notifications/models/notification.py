from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from users.models import User


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',verbose_name="Владелец")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="notify_actor",
                              on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создано")
    unread  = models.BooleanField(default=False,verbose_name="Прочитано")

    POST_REACTION = 'PR'
    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    POST_COMMENT_REACTION = 'PCRA'
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


    NOTIFICATION_TYPES = (
        (POST_REACTION, 'Рекция на пост'),
        (POST_COMMENT, 'Комментарий к посту'),
        (POST_COMMENT_REPLY, 'Ответ на комментарий к посту'),
        (POST_COMMENT_REACTION, 'Рефкция на комментарий к посту'),
        (CONNECTION_REQUEST, 'Заявка в друзья'),
        (CONNECTION_CONFIRMED, 'Одобренная заявка в друзья'),
        (FOLLOW, 'Подписка'),
        (COMMUNITY_INVITE, 'Приглашение в сообщество'),
        (POST_USER_MENTION, 'Упоминание пользователя в посте'),
        (POST_COMMENT_USER_MENTION, 'Упоминание пользователя в комментарии к посту'),
        (LIKED, 'Упоминание пользователя в лайке к посту'),
        (LIKED_COMMENT, 'Упоминание пользователя в лайке на комментарий к посту'),
        (DISLIKED, 'Упоминание пользователя в дизлайке к посту'),
        (DISLIKED_COMMENT, 'Упоминание пользователя в дизлайке на комментарий к посту'),
        (SIGNUP, 'Упоминание пользователя о созданном аккаунте'),
    )

    verb = models.CharField(max_length=5, choices=NOTIFICATION_TYPES,verbose_name="Тип уведомления")
    slug = models.SlugField(max_length=210, null=True, blank=True)
    action_object_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("action_object_content_type", "action_object_object_id")
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")
        ordering = ("-timestamp",)

    def __str__(self):
        if self.action_object:
            return f'{self.actor} {self.get_verb_display()} {self.action_object} {self.time_since()} ago'

        return f'{self.actor} {self.get_verb_display()} {self.time_since()} ago'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.recipient} {self.uuid_id} {self.verb}',
                                to_lower=True, max_length=200)

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
    Handler function to create a Notification instance.
    :requires:
    :param actor: User instance of that user who makes the action.
    :param recipient: User instance, a list of User instances or string
                      'global' defining who should be notified.
    :param verb: Notification attribute with the right choice from the list.
    :optional:
    :param action_object: Model instance on which the verb was executed.
    :param key: String defining what kind of notification is going to be created.
    :param id_value: UUID value assigned to a specific element in the DOM.
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

    elif isinstance(recipient, user):
        Notification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=kwargs.pop('action_object', None)
        )
        notification_broadcast(
            actor, key, id_value=id_value, recipient=recipient.id)

    else:
        pass


def notification_broadcast(actor, key, **kwargs):
    """Notification handler to broadcast calls to the recieve layer of the
    WebSocket consumer of this app.
    :requires:
    :param actor: User instance of that user who makes the action.
    :param key: String parameter to indicate the client which action to
                perform.
    :optional:
    :param id_value: UUID value assigned to a specific element in the DOM.
    :param recipient: String indicating the name of that who needs to be
                      notified.
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
