import uuid
from users.models import User
from django.conf import settings
from django.db import models
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from posts.models import Post
from common.utils import try_except
from pilkit.processors import ResizeToFill, ResizeToFit
from users.helpers import upload_to_user_directory
from imagekit.models import ProcessedImageField


class Chat(models.Model):
    TYPE_PRIVATE = 'PR'
    TYPE_PUBLIC = 'PU'
    TYPE_MANAGER = 'M'
    TYPES = (
        (TYPE_PRIVATE, 'Приватный чат'),
        (TYPE_PUBLIC, 'Открытый чат'),
        (TYPE_MANAGER, 'Административный чат'),
    )
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, verbose_name="Название")
    type = models.CharField(blank=False, null=False, choices=TYPES, default=TYPE_PRIVATE, max_length=4, verbose_name="Тип чата")
    image = ProcessedImageField(blank=True, format='JPEG',options={'quality': 90},upload_to=upload_to_user_directory,processors=[ResizeToFit(width=100, height=100,)])

    community = models.ForeignKey('communities.Community', related_name='community_chat', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
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

    def get_members_count(self):
        return self.get_members().values('id').count()

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
        if self.is_not_empty():
            return self.get_first_message().text
        else:
            return 'Нет сообщений'

    def get_last_message_created(self):
        if self.is_not_empty():
            return self.get_first_message().get_created()
        else:
            return ''

    def get_avatars(self):
        urls = []
        if self.image:
            urls = [self.image.url, ]
            return urls
        else:
            members = self.chat_relation.all()[:10]
            for user in members:
                urls += [user.user.get_avatar()]
        return urls

    def get_avatar(self):
        if self.image:
            return self.image.url
        count = self.get_members_count()

        if count > 2:
            return "/static/images/group_chat.png"
        elif count == 2:
            user = self.chat_relation.exclude(user_id=self.creator.pk)
            return user[0].user.get_avatar()
        elif count == 1:
            return self.creator.get_avatar()

    def get_chat_member(self, user_id):
        members = self.chat_relation.exclude(user_id=user_id)
        return members[0].user

    def get_preview(self, user_id):
        count = self.get_members_count()
        first_message = self.get_first_message()
        if count == 1:
            if self.image:
                figure = '<figure><img src="' + self.image.url + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
            if self.creator.get_avatar():
                figure = '<figure><img src="' + self.creator.get_avatar() + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
            else:
                figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = self.creator.get_full_name()
            media_body = '<div class="media-body"><h5 class="time-title mb-0">' + chat_name + \
            '<small class="float-right text-muted">' + first_message.get_created() + \
            '</small></h5><p class="mb-0">' + first_message.text + '</p></div>'
            return '<div class="media">' + figure + media_body + '</div>'
        if count == 2:
            member = self.get_chat_member(user_id)
            if self.image:
                figure = '<figure><img src="' + self.image.url + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
            if member.get_avatar():
                figure = '<figure><img src="' + member.get_avatar() + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
            else:
                figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = member.get_full_name()
            media_body = '<div class="media-body"><h5 class="time-title mb-0">' + chat_name + \
            '<small class="float-right text-muted">' + first_message.get_created() + \
            '</small></h5><p class="mb-0">' + first_message.text + '</p></div>'
            return '<div class="media">' + figure + media_body + '</div>' + self.get_unread_count_message(user_id)
        if count > 2:
            if self.image:
                figure = '<figure><img src="' + self.image.url + '"style="border-radius:50px;width:50px;" alt="image"></figure>'
            else:
                figure = '<figure><img src="/static/images/group_chat.png" style="border-radius:50px;width:50px;" alt="image"></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = "Групповой чат"
            media_body = '<div class="media-body"><h5 class="time-title mb-0">' + chat_name + \
            '<small class="float-right text-muted">' + first_message.get_created() + \
            '</small></h5><p class="mb-0">' + first_message.text + '</p></div>'
            return '<div class="media">' + figure + media_body + '</div>' + self.get_unread_count_message(user_id)


    def get_name(self, user_id):
        if self.name:
            return self.name
        count = self.get_members_count()

        if count > 2:
            a = count % 10
            b = count % 100
            if (a == 1) and (b != 11):
                return str(count) + " участник"
            elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
                return str(count) + " участника"
            else:
                return str(count) + " участников"
            return count
        elif count == 2:
            user = self.chat_relation.exclude(user_id=user_id)
            return user[0].user.get_full_name()
        elif count == 1:
            return self.creator.get_full_name()

    @classmethod
    def create_chat(cls, creator, type):
        chat = cls.objects.create(creator=creator, type=type)
        ChatUsers.create_membership(user=creator, is_administrator=True, chat=chat)
        chat.save()
        return chat

    def is_not_empty(self):
        return self.chat_message.filter(chat=self,is_deleted=False).values("pk").exists()

    def add_administrator(self, user):
        member = self.chat_relation.get(user=user)
        member.is_administrator = True
        member.save(update_fields=["is_administrator"])
        return member
    def remove_administrator(self, user):
        member = self.chat_relation.get(user=user)
        member.is_administrator = False
        member.save(update_fields=["is_administrator"])
        return member

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

    def delete_membership(user, chat):
        if ChatUsers.objects.filter(user=user, chat=chat).exists():
            membership = ChatUsers.objects.get(user=user, chat=chat)
            membership.delete()
            return HttpResponse()
        else:
            pass

    class Meta:
        unique_together = (('user', 'chat'),)
        indexes = [
            models.Index(fields=['chat', 'user']),
            models.Index(fields=['chat', 'user', 'is_administrator'])
            ]
        verbose_name = 'участник беседы'
        verbose_name_plural = 'участники бесед'


class Message(models.Model):
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_PUBLISHED = 'P'
    STATUS_EDIT = 'E'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликовано'),
        (STATUS_EDIT, 'Изменено'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(ChatUsers, related_name='message_creator', verbose_name="Создатель", null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000, blank=True)
    unread = models.BooleanField(default=True, db_index=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_thread")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_message")
    status = models.CharField(choices=STATUSES, default=STATUS_PROCESSING, max_length=5, verbose_name="Статус сообщения")

    repost = models.ForeignKey("posts.Post", on_delete=models.CASCADE, null=True, blank=True, related_name='post_message')

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

    def get_or_create_chat_and_send_message(creator, user, repost, text):
        # получаем список чатов отправителя. Если получатель есть в одном из чатов, добавляем туда сообщение.
        # Если такого чата нет, создаем приватный чат, создаем сообщение и добавляем его в чат.
        from common.processing.post import get_post_message_processing

        chat_list = creator.get_all_chats()
        current_chat = None
        for chat in chat_list:
            if user.pk in chat.get_members_ids():
                current_chat = chat
        if not current_chat:
            current_chat = Chat.objects.create(creator=creator, type=Chat.TYPE_PUBLIC)
            sender = ChatUsers.objects.create(user=creator, is_administrator=True, chat=current_chat, status=Nessage.STATUS_PROCESSING)
            ChatUsers.objects.create(user=user, chat=current_chat)
        else:
            sender = ChatUsers.objects.get(user=creator, chat=current_chat)
        new_message = Message.objects.create(chat=current_chat, creator=sender, repost=repost, text=text)
        get_post_message_processing(new_message)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'text', 'message_id': new_message.uuid, 'creator': creator, 'user': user}
        async_to_sync(channel_layer.group_send)(user.username, payload)
        return new_message

    def send_message(chat, creator, repost, parent, text):
        # программа для отсылки сообщения, когда чат известен
        from common.processing.post import get_post_message_processing

        sender = ChatUsers.objects.filter(user_id=creator.pk)[0]
        new_message = Message.objects.create(chat=chat, creator=sender, repost=repost, parent=parent, text=text, status=Nessage.STATUS_PROCESSING)
        get_post_message_processing(new_message)
        channel_layer = get_channel_layer()
        payload = {'type': 'receive', 'key': 'text', 'message_id': new_message.uuid, 'creator': creator}
        async_to_sync(channel_layer.group_send)(creator.username, payload)
        return new_message

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def is_repost(self):
        return try_except(self.repost)

    def is_photo_repost(self):
        return try_except(self.repost.status == Post.PHOTO_REPOST)
    def get_photo_repost(self):
        photo = self.repost.parent.item_photo.filter(is_deleted=False)[0]
        return photo
    def is_photo_album_repost(self):
        return try_except(self.repost.status == Post.PHOTO_ALBUM_REPOST)
    def get_photo_album_repost(self):
        photo_album = self.repost.parent.post_album.filter(is_deleted=False)[0]
        return photo_album

    def is_music_repost(self):
        return try_except(self.repost.status == Post.MUSIC_REPOST)
    def is_music_list_repost(self):
        return try_except(self.repost.status == Post.MUSIC_LIST_REPOST)
    def get_playlist_repost(self):
        playlist = self.repost.parent.post_soundlist.filter(is_deleted=False)[0]
        return playlist
    def get_music_repost(self):
        music = self.repost.parent.item_music.filter(is_deleted=False)[0]
        return music

    def is_good_repost(self):
        return try_except(self.repost.status == Post.GOOD_REPOST)
    def is_good_list_repost(self):
        return try_except(self.repost.status == Post.GOOD_LIST_REPOST)
    def get_good_repost(self):
        good = self.repost.item_good.filter(is_deleted=False)[0]
        return good
    def get_good_list_repost(self):
        good_list = self.repost.parent.post_good_album.filter(is_deleted=False)[0]
        return good_list

    def is_doc_repost(self):
        return try_except(self.repost.status == Post.DOC_REPOST)
    def is_doc_list_repost(self):
        return try_except(self.repost.status == Post.DOC_LIST_REPOST)
    def get_doc_list_repost(self):
        list = self.repost.parent.post_doclist.filter(is_deleted=False)[0]
        return list
    def get_doc_repost(self):
        doc = self.repost.parent.item_doc.filter(is_deleted=False)[0]
        return doc

    def is_video_repost(self):
        return try_except(self.repost.status == Post.VIDEO_REPOST)
    def is_video_list_repost(self):
        return try_except(self.repost.status == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        video_list = self.repost.parent.post_video_album.filter(is_deleted=False)[0]
        return video_list

    def get_attach_photos(self):
        return self.message_photo.filter(is_deleted=False)
    def get_attach_photo_list(self):
        return self.message_album.filter(is_deleted=False)
    def get_attach_videos(self):
        return self.message_video.filter(is_deleted=False)
    def get_attach_video_list(self):
        return self.message_video_album.filter(is_deleted=False)
    def get_attach_goods(self):
        return self.message_good.filter(is_deleted=False)
    def get_attach_good_list(self):
        return self.message_good_album.filter(is_deleted=False)
    def get_attach_articles(self):
        return self.attached_message.filter(is_deleted=False)
    def get_attach_tracks(self):
        return self.message_music.filter(is_deleted=False)
    def get_attach_music_list(self):
        return self.message_soundlist.filter(is_deleted=False)
    def get_attach_docs(self):
        return self.message_doc.filter(is_deleted=False)
    def get_attach_doc_list(self):
        return self.message_doclist.filter(is_deleted=False)

    def is_photo_list_attached(self):
        return self.message_album.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_playlist_attached(self):
        return self.message_soundlist.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_video_list_attached(self):
        return self.message_video_album.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_good_list_attached(self):
        return self.message_good_album.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_doc_list_attached(self):
        return self.message_doclist.filter(post__pk=self.pk, is_deleted=False).exists()

    def get_c_repost_items(self):
        # метод выясняет, есть ли у поста-родителя в сообществе прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
        repost = self.repost
        if repost.is_photo_repost():
            return "post_community/photo_repost.html"
        elif repost.is_photo_album_repost():
            return "post_community/photo_album_repost.html"
        if repost.is_photo_list_attached():
            return "generic/parent_attach/c_photo_list_attach.html"
        elif repost.is_good_repost():
            return "post_community/good_repost.html"
        elif repost.is_good_list_repost():
            return "post_community/good_list_repost.html"
        elif repost.is_good_list_attached():
            return "generic/parent_attach/c_good_list_attach.html"
        elif repost.is_music_repost():
            return "post_community/music_repost.html"
        elif repost.is_music_list_repost():
            return "post_community/music_list_repost.html"
        elif repost.is_playlist_attached():
            return "generic/parent_attach/c_playlist_attach.html"
        elif repost.is_video_repost():
            return "post_community/video_repost.html"
        elif repost.is_video_list_repost():
            return "post_community/video_list_repost.html"
        elif repost.is_video_list_attached():
            return "generic/parent_attach/c_video_list_attach.html"
        elif repost.is_doc_repost():
            return "post_community/doc_repost.html"
        elif repost.is_doc_list_repost():
            return "post_community/doc_list_repost.html"
        elif repost.is_doc_list_attached():
            return "generic/parent_attach/c_doc_list_attach.html"
        elif repost.is_user_repost():
            return "post_community/user_repost.html"
        elif repost.is_community_repost():
            return "post_community/community_repost.html"
        else:
            return "generic/attach/parent_community.html"

    def get_u_repost_items(self):
        # метод выясняет, есть ли у поста-родителя пользователя прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
        repost = self.repost
        if repost.is_photo_repost():
            return "post_user/photo_repost.html"
        elif repost.is_photo_album_repost():
            return "post_user/photo_album_repost.html"
        if repost.is_photo_list_attached():
            return "generic/parent_attach/u_photo_list_attach.html"
        elif repost.is_good_repost():
            return "post_user/good_repost.html"
        elif repost.is_good_list_repost():
            return "post_user/good_list_repost.html"
        elif repost.is_good_list_attached():
            return "generic/parent_attach/u_good_list_attach.html"
        elif repost.is_music_repost():
            return "post_user/music_repost.html"
        elif repost.is_music_list_repost():
            return "post_user/music_list_repost.html"
        elif repost.is_playlist_attached():
            return "generic/parent_attach/u_playlist_attach.html"
        elif repost.is_video_repost():
            return "post_user/video_repost.html"
        elif repost.is_video_list_repost():
            return "post_user/video_list_repost.html"
        elif repost.is_video_list_attached():
            return "generic/parent_attach/u_video_list_attach.html"
        elif repost.is_doc_repost():
            return "post_user/doc_repost.html"
        elif repost.is_doc_list_repost():
            return "post_user/doc_list_repost.html"
        elif repost.is_doc_list_attached():
            return "generic/parent_attach/u_doc_list_attach.html"
        elif repost.is_user_repost():
            return "post_user/user_repost.html"
        elif repost.is_community_repost():
            return "post_user/community_repost.html"
        else:
            return "generic/attach/parent_user.html"

    def get_attach_items(self):
        if self.is_photo_list_attached():
            return "generic/attach/u_photo_list_attach.html"
        elif self.is_playlist_attached():
            return "generic/attach/u_playlist_attach.html"
        elif self.is_video_list_attached():
            return "generic/attach/u_video_list_attach.html"
        elif self.is_good_list_attached():
            return "generic/attach/u_good_list_attach.html"
        elif self.is_doc_list_attached():
            return "generic/attach/u_doc_list_attach.html"
        else:
            return "generic/attach/u_post_attach.html"

    def get_fixed_message_for_chat(self, chat_id):
        try:
            message = Message.objects.get(chat_id=chat_id, is_fixed=True)
            message.is_fixed = False
            message.save(update_fields=['is_fixed'])
            new_fixed = Message.objects.get(pk=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])
        except:
            new_fixed = Message.objects.get(pk=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])


class MessageFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_message_favorite', verbose_name="Члены сообщества")
    message = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_favorite', verbose_name="Члены сообщества")

    class Meta:
        unique_together = (('user', 'message'),)
        verbose_name = 'Избранное сообщение'
        verbose_name_plural = 'Избранные сообщения'

    @classmethod
    def create_favorite(cls, user_id, message):
        if not cls.objects.filter(user_id=user_id, message=message).exists():
            favorite = cls.objects.create(user_id=user_id, message=message,)
            return favorite
        else:
            pass
