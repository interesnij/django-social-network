import uuid
from users.models import User
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone


class MessageQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability."""

    def get_conversation(self, sender, recipient):
        """Возвращает все сообщения, отправленные между двумя пользователями."""
        qs_one = self.filter(sender=sender, recipient=recipient)
        qs_two = self.filter(sender=recipient, recipient=sender)
        return qs_one.union(qs_two).order_by('created')

    def get_most_recent_conversation(self, recipient):
        """Возвращает имя пользователя самого последнего собеседника."""
        try:
            qs_sent = self.filter(sender=recipient)
            qs_recieved = self.filter(recipient=recipient)
            qs = qs_sent.union(qs_recieved).latest("created")
            if qs.sender == recipient:
                return qs.recipient

            return qs.sender

        except self.model.DoesNotExist:
            return User.objects.get(id=recipient.id)

    def mark_conversation_as_read(self, sender, recipient):
        """Отметьте как прочитанные все непрочитанные элементы в текущем разговоре."""
        qs = self.filter(sender=sender, recipient=recipient)
        return qs.update(unread=False)


class Chat(models.Model):
    TYPE_PRIVATE = 'PR'
    TYPE_PUBLIC = 'PU'
    TYPE_MANAGER = 'M'
    TYPES = (
        (COMMUNITY_TYPE_PUBLIC, 'Приватный чат'),
        (COMMUNITY_TYPE_PRIVATE, 'Коллективный чат'),
        (COMMUNITY_TYPE_CLOSED, 'Административный чат'),
    )
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(blank=False, null=False, choices=TYPES, default=COMMUNITY_TYPE_PRIVATE, max_length=4, verbose_name="Тип чата")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_creator', null=True, blank=False, verbose_name="Создатель")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"
        ordering = "-created",
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.message

    def is_private(self):
        return self.type == Chat.TYPE_PRIVATE
    def is_public(self):
        return self.type == Chat.TYPE_PUBLIC
    def is_manager(self):
        return self.type == Chat.TYPE_MANAGER

    @classmethod
    def create_chat(cls, creator, type):
        chat = cls.objects.create(creator=creator, type=type)
        ChatUsers.create_membership(user=creator, is_administrator=True, chat=chat)
        chat.save()
        return chat

    def user_exists(self, user_1, user_2):
        a = self.chat_users.filter(user=user_1).exists()
        b = self.chat_users.filter(user=user_2).exists()
        if a and b and self.is_private():
            return self


class ChatUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='chat_users', null=False, blank=False, verbose_name="Члены сообщества")
    chat = models.ForeignKey(Chat, db_index=False, on_delete=models.CASCADE, related_name='chat_relation', verbose_name="Чат")
    is_administrator = models.BooleanField(default=False, verbose_name="Это администратор")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_membership(cls, user, chat, is_administrator=False):
        membership = cls.objects.create(user=user, chat=chat, is_administrator=is_administrator)
        return membership

    class Meta:
        unique_together = (('user', 'chat'),)
        indexes = [
            models.Index(fields=['chat', 'user']),
            models.Index(fields=['chat', 'user', 'is_administrator'])
            ]
        verbose_name = 'участник беседы'
        verbose_name_plural = 'участники бесед'



class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(ChatUsers, related_name='sent_user', verbose_name="Отправитель", null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(ChatUsers, related_name='received_user', null=True, blank=True, verbose_name="Получатель", on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000, blank=True)
    unread = models.BooleanField(default=True, db_index=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_thread")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_message")
    objects = MessageQuerySet.as_manager()

    post = models.ManyToManyField("posts.Post", blank=True, related_name='post_message')

    class Meta:
        verbose_name = "Сооьщение"
        verbose_name_plural = "Сооьщения"
        ordering = "-created",
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    @staticmethod
    def send_private_message(cls, sender, recipient, parent, message):
        if ChatUsers.user_exists(sender):
            chat = Chat.objects.get(chat__user=sender)
        else:
            chat = Chat.create_chat(user=sender, type=Chat.TYPE_PRIVATE)
            ChatMembership.objects.create(user=recipient, chat=chat)
        new_message = cls.objects.create(chat=chat, sender=sender, parent=parent, recipient=recipient, message=message)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'message', 'message_id': new_message.uuid, 'sender': sender, 'recipient': recipient}
        async_to_sync(channel_layer.group_send)(recipient.username, payload)
        return new_message

    @staticmethod
    def send_public_message(cls, chat, sender, parent, message):
        new_message = cls.objects.create(chat=chat, sender=sender, parent=parent, message=message)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'message', 'message_id': new_message.uuid, 'sender': sender,}
        async_to_sync(channel_layer.group_send)(sender.username, payload)
        return new_message

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)
