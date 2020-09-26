import uuid
from users.models import User
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from posts.models import Post
from common.utils import try_except


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
        return self.chat_message.filter(is_deleted=False).last()

    def get_messages(self):
        return self.chat_message.filter(is_deleted=False)

    def get_unread_count_message(self, user_id):
        count = self.chat_message.filter(is_deleted=False, unread=True).exclude(creator__user_id=user_id).values("pk").count()
        if count:
            return '<span class="icon-rounded icon-40 bg-danger ml-2">' + str(count) + '</span>'
        else:
            return ""

    def get_unread_message(self, user_id):
        return self.chat_message.filter(is_deleted=False, unread=True).exclude(creator__user_id=user_id)

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

    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, blank=True, related_name='post_message') 

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = "created",
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

    def is_repost(self):
        return try_except(self.post)

    def is_photo_repost(self):
        return try_except(self.post_message.status == Post.PHOTO_REPOST)
    def get_photo_repost(self):
        photo = self.post_message.parent.item_photo.all()[0]
        return photo
    def is_photo_album_repost(self):
        return try_except(self.post_message.status == Post.PHOTO_ALBUM_REPOST)
    def get_photo_album_repost(self):
        photo_album = self.post_message.parent.post_album.all()[0]
        return photo_album

    def is_music_repost(self):
        return try_except(self.post_message.status == Post.MUSIC_REPOST)
    def is_music_list_repost(self):
        return try_except(self.post_message.status == Post.MUSIC_LIST_REPOST)
    def get_playlist_repost(self):
        playlist = self.post_message.parent.post_soundlist.all()[0]
        return playlist
    def get_music_repost(self):
        music = self.post_message.parent.item_music.all()[0]
        return music

    def is_good_repost(self):
        return try_except(self.post_message.status == Post.GOOD_REPOST)
    def is_good_list_repost(self):
        return try_except(self.post_message.status == Post.GOOD_LIST_REPOST)
    def get_good_repost(self):
        good = self.post_message.parent.item_good.all()[0]
        return good
    def get_good_list_repost(self):
        good_list = self.post_message.parent.post_good_album.all()[0]
        return good_list

    def is_doc_repost(self):
        return try_except(self.post_message.status == Post.DOC_REPOST)
    def is_doc_list_repost(self):
        return try_except(self.post_message.status == Post.DOC_LIST_REPOST)
    def get_doc_list_repost(self):
        list = self.post_message.parent.post_doclist.all()[0]
        return list
    def get_doc_repost(self):
        doc = self.post_message.parent.item_doc.all()[0]
        return doc

    def is_video_repost(self):
        return try_except(self.post_message.status == Post.VIDEO_REPOST)
    def is_video_list_repost(self):
        return try_except(self.post_message.status == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        video_list = self.post_message.parent.post_video_album.all()[0]
        return video_list

    def get_attach_photos(self):
        return self.message_photo.all()
    def get_attach_photo_list(self):
        return self.message_album.all()
    def get_attach_videos(self):
        return self.message_video.all()
    def get_attach_video_list(self):
        return self.message_video_album.all()
    def get_attach_goods(self):
        return self.message_good.all()
    def get_attach_good_list(self):
        return self.message_good_album.all()
    def get_attach_articles(self):
        return self.attached_message.all()
    def get_attach_tracks(self):
        return self.message_music.all()
    def get_attach_music_list(self):
        return self.message_soundlist.all()
    def get_attach_docs(self):
        return self.message_doc.all()
    def get_attach_doc_list(self):
        return self.message_doclist.all()

    def is_photo_list_attached(self):
        return self.message_album.filter(post__pk=self.pk).exists()
    def is_playlist_attached(self):
        return self.message_soundlist.filter(post__pk=self.pk).exists()
    def is_video_list_attached(self):
        return self.message_video_album.filter(post__pk=self.pk).exists()
    def is_good_list_attached(self):
        return self.message_good_album.filter(post__pk=self.pk).exists()
    def is_doc_list_attached(self):
        return self.message_doclist.filter(post__pk=self.pk).exists()

    def get_items(self):
        # метод выясняет, есть ли у сообщения прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
        parent = self
        if self.post.is_photo_repost():
            return "message/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "message/photo_album_repost.html"
        if self.is_photo_list_attached():
            return "generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "message/good_repost.html"
        elif parent.is_good_list_repost():
            return "message/good_list_repost.html"
        elif self.is_good_list_attached():
            return "generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "message/music_repost.html"
        elif parent.is_music_list_repost():
            return "message/music_list_repost.html"
        elif self.is_playlist_attached():
            return "generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "message/video_repost.html"
        elif parent.is_video_list_repost():
            return "message/video_list_repost.html"
        elif self.is_video_list_attached():
            return "generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "message/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "message/doc_list_repost.html"
        elif self.is_doc_list_attached():
            return "generic/parent_attach/u_doc_list_attach.html"
        else:
            return "message/parent_user.html"
