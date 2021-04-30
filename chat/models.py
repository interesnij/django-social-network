import uuid
from django.conf import settings
from django.db import models
from common.utils import try_except
from pilkit.processors import ResizeToFill, ResizeToFit
from chat.helpers import upload_to_chat_directory, validate_file_extension
from imagekit.models import ProcessedImageField
from django.contrib.postgres.indexes import BrinIndex


class Chat(models.Model):
    LIST, MANAGER, THIS_PROCESSING, PRIVATE, THIS_FIXED = 'LIS', 'MAN', 'TPRO', 'PRI', 'TFIX'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = 'TDEL', 'TDELP', 'TDELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER, THIS_CLOSED_FIXED = 'TCLO', 'TCLOP', 'TCLOM', 'TCLOMA', 'TCLOF'
    TYPE = (
        (LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),(THIS_FIXED, 'Закреплённый'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),(THIS_CLOSED_FIXED, 'Закрытый закреплённый'),
    )
    name = models.CharField(max_length=100, blank=True, verbose_name="Название")
    type = models.CharField(blank=False, null=False, choices=TYPE, default=THIS_PROCESSING, max_length=6, verbose_name="Тип чата")
    image = ProcessedImageField(blank=True, format='JPEG',options={'quality': 100},upload_to=upload_to_chat_directory,processors=[ResizeToFit(width=100, height=100,)])
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    community = models.ForeignKey('communities.Community', related_name='community_chat', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_creator', null=True, blank=False, verbose_name="Создатель")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    def is_private(self):
        return self.type == Chat.PRIVATE
    def is_public(self):
        return self.type == Chat.LIST
    def is_manager(self):
        return self.type == Chat.MANAGER
    def is_open(self):
        return self.type[0] != "T"

    def get_members(self):
        from users.models import User
        members = User.objects.filter(chat_users__chat__pk=self.pk)
        return members

    def get_members_ids(self):
        users = self.get_members().values('id')
        return [_user['id'] for _user in users]

    def get_members_count(self):
        return self.get_members().values('id').count()

    def get_first_message(self):
        return self.chat_message.exclude(status__contains="THIS").last()

    def get_messages(self):
        return self.chat_message.exclude(status__contains="THIS")

    def get_messages_uuids(self):
        messages = self.chat_message.exclude(status__contains="THIS").values('uuid')
        return [i['uuid'] for i in messages]

    def get_attach_photos(self):
        from gallery.models import Photo
        return Photo.objects.filter(message__uuid__in=self.get_messages_uuids())

    def get_unread_count_message(self, user_id):
        count = self.chat_message.filter(unread=True).exclude(status__contains="THIS", creator__user_id=user_id).values("pk").count()
        if count:
            return ''.join(['<span style="font-size: 80%;" class="tab_badge badge-success">', str(count), '</span>'])
        else:
            return ""

    def get_unread_message(self, user_id):
        return self.chat_message.filter(unread=True).exclude(creator__user_id=user_id, status__contains="THIS")

    def get_last_message_created(self):
        if self.is_not_empty():
            return self.get_first_message().get_created()
        else:
            return ''

    def get_chat_member(self, user_id):
        members = self.chat_relation.exclude(user_id=user_id)
        return members[0].user
    def get_chat_user(self, user_id):
        members = self.chat_relation.filter(user_id=user_id)
        return members[0].user

    def get_preview_message(self, user_id):
        count = self.get_members_count()
        first_message = self.get_first_message()
        creator_figure = ''
        if count == 1:
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            elif self.creator.get_avatar():
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            else:
                figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = self.creator.get_full_name()
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">',chat_name, '<span class="status bg-success"></span><small class="float-right text-muted">', first_message.get_created(), '</small></h5><p class="mb-0" style="white-space: nowrap;">', first_message.get_preview_text(), '</p></div>'])
            return ''.join(['<div class="media">', figure, media_body, '</div>'])
        elif count == 2:
            member = self.get_chat_member(user_id)
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            elif member.get_avatar():
                figure = ''.join(['<figure><img src="', member.s_avatar.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            else:
                figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = member.get_full_name()
            if member.get_online():
                status = ' <span class="status bg-success"></span>'
            else:
                status = ''
            if first_message.creator.user_id == user_id:
                creator_figure = '<span class="underline">Вы:</span> '
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, status, '<small class="float-right text-muted">', first_message.get_created(), '</small></h5><p class="mb-0" style="white-space: nowrap;">', creator_figure, first_message.get_preview_text(), '</p></div>'])
            return ''.join(['<div class="media">', figure, media_body, self.get_unread_count_message(user_id), '</div>'])
        elif count > 2:
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            else:
                figure = '<figure><img src="/static/images/group_chat.jpg" style="border-radius:50px;width:50px;" alt="image"></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = "Групповой чат"
            if first_message.creator.user_id == user_id:
                creator_figure = '<span class="underline">Вы:</span> '
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, '<small class="float-right text-muted">', first_message.get_created(), '</small></h5><p class="mb-0" style="white-space: nowrap;">', creator_figure, first_message.get_preview_text(), '</p></div>'])
            return ''.join(['<div class="media">', figure, media_body, self.get_unread_count_message(user_id), '</div>'])

    def get_avatars(self):
        urls = []
        for user in self.chat_relation.all()[:10]:
            urls += [user.user.s_avatar.url]
        return urls

    def get_header_chat(self, user_id):
        count = self.get_members_count()
        buttons = '<span class="settings_btn" style="display:none"><svg fill="currentColor" class="svg_default svg_default_25 mr-1 pointer" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg><svg fill="currentColor" class="svg_default svg_default_25 mr-1 pointer" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z"fill="none"/></svg></span>'
        if count == 2:
            member = self.get_chat_member(user_id)
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            elif member.get_avatar():
                figure = ''.join(['<figure><a href="/users/', str(member.pk),'" class="ajax"><img src="', member.s_avatar.url,'" style="border-radius:50px;width:50px;" alt="image"></a></figure>'])
            else:
                figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = member.get_full_name()
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, '</h5><p class="mb-0 target_display"><span class="type_display">', self.get_type_display(), '</span>', buttons, '</p></div>'])
            return ''.join([figure, media_body])
        elif count > 2:
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            else:
                avatars = ''
                for figure in self.get_avatars():
                    if figure:
                        avatars = ''.join([avatars, '<figure><img src="', figure, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
                    else:
                        avatars = ''.join([avatars, '<figure class="avatar-50 staked"><img src="/static/images/no_img/user.jpg" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            if self.name:
                 chat_name = self.name
            else:
                chat_name = "Групповой чат"
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, + '</h5><p class="mb-0 target_display"><span class="type_display">', self.get_type_display(), '</span>', buttons, '</p></div>'])
            return ''.join([avatars, media_body])
        elif count == 1:
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            elif self.creator.get_avatar():
                figure = ''.join(['<figure><img src="', self.creator.s_avatar.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            else:
                figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = self.creator.get_full_name()
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, '</h5><p class="mb-0 target_display"><span class="type_display">', self.get_type_display(), '</span>', buttons, '</p></div>'])
            return ''.join([figure, media_body])

    def is_not_empty(self):
        return self.chat_message.exclude(status__contains="THIS").values("pk").exists()

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
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")

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
    THIS_PROCESSING, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = 'PRO','PUB','PRI','MAN','TDEL','TCLO'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = 'TDELP','TDELM','TCLOP','TCLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(ChatUsers, related_name='message_creator', verbose_name="Создатель", null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000, blank=True)
    unread = models.BooleanField(default=True, db_index=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_thread")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_message")
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5, verbose_name="Статус сообщения")
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    voice = models.FileField(blank=True, upload_to=upload_to_chat_directory, verbose_name="Голосовое сообщение")

    #repost = models.ForeignKey("posts.Post", on_delete=models.CASCADE, null=True, blank=True, related_name='post_message')

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

    def get_creator(self):
        return self.creator.user

    def get_reseiver_ids(self):
        return self.chat.get_members_ids()

    def create_socket(self):
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'message',
            'message_id': str(self.uuid),
            'creator_id': self.creator.user.pk,
            'chat_id': self.chat.pk,
            'reseiver_ids': self.get_reseiver_ids(),
            'name': "u_message_create",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


    def get_or_create_chat_and_send_message(creator, user, repost, text, attach, voice):
        # получаем список чатов отправителя. Если получатель есть в одном из чатов, добавляем туда сообщение.
        # Если такого чата нет, создаем приватный чат, создаем сообщение и добавляем его в чат.
        from common.processing.message import get_message_processing

        chat_list, current_chat = creator.get_all_chats(), None
        for chat in chat_list:
            if user.pk in chat.get_members_ids():
                current_chat = chat
        if not current_chat:
            current_chat = Chat.objects.create(creator=creator, type=Chat.TYPE_PUBLIC)
            sender = ChatUsers.objects.create(user=creator, is_administrator=True, chat=current_chat)
            ChatUsers.objects.create(user=user, chat=current_chat)
        else:
            sender = ChatUsers.objects.get(user=creator, chat=current_chat)
        if voice:
            new_message = Message.objects.create(chat=current_chat, creator=sender, repost=repost, voice=voice, status=Message.STATUS_PROCESSING)
        else:
            _attach = str(attach)
            _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
            new_message = Message.objects.create(chat=current_chat, creator=sender, repost=repost, text=text, attach=_attach, status=Message.STATUS_PROCESSING)
        new_message = Message.objects.create(chat=current_chat, creator=sender, repost=repost, text=text, status=Message.STATUS_PROCESSING)
        get_message_processing(new_message)
        new_message.create_socket()
        return new_message

    def create_chat_append_members_and_send_message(creator, users_ids, text, attach, voice):
        # Создаем коллективный чат и добавляем туда всех пользователй из полученного списка
        from common.processing.message import get_message_processing

        chat = Chat.objects.create(creator=creator, type=Chat.TYPE_PUBLIC)
        sender = ChatUsers.objects.create(user=creator, is_administrator=True, chat=chat)
        for user_id in users_ids:
            ChatUsers.objects.create(user_id=user_id, chat=chat)
        if voice:
            new_message = Message.objects.create(chat=chat, creator=sender, voice=voice, status=Message.STATUS_PROCESSING)
        else:
            _attach = str(attach)
            _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
            new_message = Message.objects.create(chat=chat, creator=sender, attach=_attach, text=text, status=Message.STATUS_PROCESSING)
        get_message_processing(new_message)
        new_message.create_socket()
        return new_message

    def send_message(chat, creator, repost, parent, text, attach, voice):
        # программа для отсылки сообщения в чате
        from common.processing.message import get_message_processing

        sender = ChatUsers.objects.filter(user_id=creator.pk)[0]
        if voice:
            new_message = Message.objects.create(chat=chat, creator=sender, repost=repost, parent=parent, voice=voice, status=Message.STATUS_PROCESSING)
        else:
            _attach = str(attach)
            _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
            new_message = Message.objects.create(chat=chat, creator=sender, repost=repost, parent=parent, text=text, attach=_attach, status=Message.STATUS_PROCESSING)
        get_message_processing(new_message)
        new_message.create_socket()
        return new_message

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_preview_text(self):
        if self.attach and self.text:
            return "Текст и вложения"
        elif self.attach and not self.text:
            return "Вложения"
        else:
            return self.text[:60]

    def is_repost(self):
        return try_except(self.repost)

    def is_photo_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.PHOTO_REPOST)
    def get_photo_repost(self):
        photo = self.repost.parent.item_photo.filter(is_deleted=False)[0]
        return photo
    def is_photo_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.PHOTO_LIST_REPOST)
    def get_photo_list_repost(self):
        return self.repost.parent.post_list.filter(is_deleted=False)[0]

    def is_music_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.MUSIC_REPOST)
    def is_music_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.MUSIC_LIST_REPOST)
    def get_playlist_repost(self):
        playlist = self.repost.parent.post_soundlist.exclude(type__contains="THIS")[0]
        return playlist
    def get_music_repost(self):
        music = self.repost.parent.item_music.exclude(type__contains="THIS")[0]
        return music

    def is_good_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.GOOD_REPOST)
    def is_good_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.GOOD_LIST_REPOST)
    def get_good_repost(self):
        return self.repost.item_good.exclude(type__contains="THIS")[0]
    def get_good_list_repost(self):
        return self.repost.parent.post_good_list.exclude(type__contains="THIS")[0]

    def is_doc_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.DOC_REPOST)
    def is_doc_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.DOC_LIST_REPOST)
    def get_doc_list_repost(self):
        return self.repost.parent.post_doclist.exclude(type__contains="THIS")[0]
    def get_doc_repost(self):
        return self.repost.parent.item_doc.exclude(type__contains="THIS")[0]

    def is_video_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.VIDEO_REPOST)
    def is_video_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.status == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        return self.repost.parent.post_video_list.exclude(type__contains="THIS")[0]

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

    def get_u_message_parent(self, user):
        from common.attach.message_attach import get_u_message_parent
        return get_u_message_parent(self.parent, user)

    def get_c_message_parent(self, user):
        from common.attach.message_attach import get_c_message_parent
        return get_c_message_parent(self.parent, user)

    def get_u_attach(self, user):
        from common.attach.message_attach import get_u_message_attach
        return get_u_message_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.message_attach import get_c_message_attach
        return get_c_message_attach(self, user)
