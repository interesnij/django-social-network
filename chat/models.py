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
        (TYPE_PRIVATE, 'Приватный чат'),
        (TYPE_PUBLIC, 'Коллективный чат'),
        (TYPE_MANAGER, 'Административный чат'),
    )
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(blank=False, null=False, choices=TYPES, default=TYPE_PRIVATE, max_length=4, verbose_name="Тип чата")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_creator', null=True, blank=False, verbose_name="Создатель")
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")

    class Meta:
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"
        ordering = "-created",
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    def is_private(self):
        return self.type == Chat.TYPE_PRIVATE
    def is_public(self):
        return self.type == Chat.TYPE_PUBLIC
    def is_manager(self):
        return self.type == Chat.TYPE_MANAGER

    def get_members(self):
        members = User.objects.filter(chat_users__chat__pk=self.pk)
        return members

    def get_members_ids(self):
        users = self.get_members().values('id')
        users_ids = [_user['id'] for _user in users]
        return users_ids

    def get_first_message(self):
        return self.chat_message.filter(is_deleted=False).first()

    def get_unread_count_message(self, user_id):
        count = self.chat_message.filter(is_deleted=False, unread=True).exclude(creator__user_id=user_id).values("pk").count()
        if count:
            return '<span class="icon-rounded icon-40 bg-danger ml-2">' + str(count) + '</span>'
        else:
            return ""

    def get_preview(self):
        return self.get_first_message().text

    def get_two_members(self):
        two = self.chat_relation.exclude()[:2]
        return str(two[0]) + ", " + str(two[1])

    @classmethod
    def create_chat(cls, creator, type):
        chat = cls.objects.create(creator=creator, type=type)
        ChatUsers.create_membership(user=creator, is_administrator=True, chat=chat)
        chat.save()
        return chat

    def is_not_empty(self):
        return self.chat_message.filter(chat=self).values("pk").exists()


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
    creator = models.ForeignKey(ChatUsers, related_name='message_creator', verbose_name="Создатель", null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000, blank=True)
    unread = models.BooleanField(default=True, db_index=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_thread")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_message")
    objects = MessageQuerySet.as_manager()

    post = models.ManyToManyField("posts.Post", blank=True, related_name='post_message')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = "-created",
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.text

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def get_or_create_chat_and_send_message(creator, user, text):
        # получаем список чатов отправителя. Если получатель есть в одном из чатов, добавляем туда сообщение.
        # Если такого чата нет, создаем приватный чат, создаем сообщение и добавляем его в чат.
        chat_list = creator.get_all_chats()
        current_chat = None
        for chat in chat_list:
            if user.pk in chat.get_members_ids():
                current_chat = chat
        if not current_chat:
            current_chat = Chat.objects.create(creator=creator, type=Chat.TYPE_PRIVATE)
            sender = ChatUsers.objects.create(user=creator, is_administrator=True, chat=current_chat)
            ChatUsers.objects.create(user=user, chat=current_chat)
        else:
            sender = ChatUsers.objects.get(user=creator, chat=current_chat)
        new_message = Message.objects.create(chat=current_chat, creator=sender, parent=None, text=text)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'text', 'message_id': new_message.uuid, 'creator': creator, 'user': user}
        async_to_sync(channel_layer.group_send)(user.username, payload)
        return new_message

    def send_message(chat, creator, parent, text):
        # программа для отсылки сообщения, когда чат известен
        sender = ChatUsers.objects.get(user=creator)
        new_message = Message.objects.create(chat=chat, creator=sender, parent=parent, text=text)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'text', 'message_id': new_message.uuid, 'creator': creator}
        async_to_sync(channel_layer.group_send)(creator.username, payload)
        return new_message

    def send_public_message(chat, creator, parent, text):
        # отсылка сообщений в групповой чат
        sender = ChatUsers.objects.get(user=creator)
        new_message = Chat.objects.create(chat=chat, creator=sender, parent=parent, text=text)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'text', 'message_id': new_message.uuid, 'creator': creator,}
        async_to_sync(channel_layer.group_send)(creator.username, payload)
        return new_message

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)
