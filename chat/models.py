import uuid
from django.conf import settings
from django.db import models
from common.utils import try_except
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from chat.helpers import upload_to_chat_directory, validate_file_extension
from imagekit.models import ProcessedImageField
from django.contrib.postgres.indexes import BrinIndex
from django.db.models import Q
from common.model.other import Stickers


class Chat(models.Model):
    PUBLIC,PRIVATE,MANAGER,GROUP,SUPPORT = 'PUB','PRI','MAN','GRO','SUP'
    DELETED_PUBLIC,DELETED_PRIVATE,DELETED_MANAGER,DELETED_GROUP,DELETED_SUPPORT = '_DPUB','_DPRI','_DMAN','_DGRO','_DSUP'
    CLOSED_PUBLIC,CLOSED_PRIVATE,CLOSED_MANAGER,CLOSED_GROUP,CLOSED_SUPPORT = '_CPUB','_CPRI','_CMAN','_CGRO','_CSUP'
    ALL_CAN, CREATOR, CREATOR_ADMINS, MEMBERS_BUT, SOME_MEMBERS = 1,2,3,4,5

    TYPE = (
        (PUBLIC, 'Публичный'),(PRIVATE, 'Приватный'),(MANAGER, 'Служебный'),(GROUP, 'Групповой'),(SUPPORT, 'Техподдержка'),
        (DELETED_PUBLIC, 'удал Публичный'),(DELETED_PRIVATE, 'удал Приватный'),(DELETED_MANAGER, 'удал Служебный'),(DELETED_GROUP, 'удал Групповой'),(DELETED_SUPPORT, 'удал Техподдержка'),
        (CLOSED_PUBLIC, 'закр. Публичный'),(CLOSED_PRIVATE, 'закр. Приватный'),(CLOSED_MANAGER, 'закр. Служебный'),(CLOSED_GROUP, 'закр. Групповой'),(CLOSED_SUPPORT, 'закр. Техподдержка'),
    )
    ALL_PERM = ((ALL_CAN, 'Все участники'),(CREATOR, 'Создатель'),(CREATOR_ADMINS, 'Создатель и админы'),(MEMBERS_BUT, 'Участники кроме'),(SOME_MEMBERS, 'Некоторые участники'),)

    name = models.CharField(max_length=100, blank=True, verbose_name="Название")
    type = models.CharField(blank=False, null=False, choices=TYPE, max_length=6, verbose_name="Тип чата")
    image = models.ImageField(blank=True, upload_to=upload_to_chat_directory)
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    community = models.ForeignKey('communities.Community', related_name='community_chat', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_creator', null=True, blank=False, verbose_name="Создатель")
    created = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    members = models.PositiveIntegerField(default=0)
    attach = models.TextField(blank=True,null=True)

    """ Полномочия в чате """
    can_add_members = models.PositiveSmallIntegerField(choices=ALL_PERM, default=1, verbose_name="Кто приглашает участников")
    can_fix_item = models.PositiveSmallIntegerField(choices=ALL_PERM, default=3, verbose_name="Кто закрепляет сообщения")
    can_mention = models.PositiveSmallIntegerField(choices=ALL_PERM, default=1, verbose_name="Кто упоминает о беседе")
    can_add_admin = models.PositiveSmallIntegerField(choices=ALL_PERM, default=3, verbose_name="Кто назначает админов")
    can_add_design = models.PositiveSmallIntegerField(choices=ALL_PERM, default=3, verbose_name="Кто меняет дизайн")
    can_see_settings = models.PositiveSmallIntegerField(choices=ALL_PERM, default=2, verbose_name="Кто видит настройки")
    can_see_log = models.PositiveSmallIntegerField(choices=ALL_PERM, default=2, verbose_name="Кто видит логи")

    class Meta:
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-created"]

    def __str__(self):
        return self.creator.get_full_name()

    def post_include_users(self, users, type):
        if type == "can_add_members":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_in_chat=1).update(can_add_in_chat=0)
        elif type == "can_fix_item":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_fix=1).update(can_add_fix=0)
        elif type == "can_add_admin":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_admin=1).update(can_add_admin=0)
        elif type == "can_mention":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_send_mention=1).update(can_send_mention=0)
        elif type == "can_add_design":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_design=1).update(can_add_design=0)
        elif type == "can_see_settings":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_see_settings=1).update(can_see_settings=0)
        elif type == "can_see_log":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_see_log=1).update(can_see_log=0)
        for user_id in users:
            member = self.chat_relation.filter(user_id=user_id).first()
            if ChatPerm.objects.filter(user_id=member.pk).exists():
                perm = ChatPerm.objects.get(user_id=member.pk)
            else:
                perm = ChatPerm.objects.create(user_id=member.pk)
            if type == "can_add_members":
                perm.can_add_in_chat = 1
                self.can_add_members = 5
                self.save(update_fields=["can_add_members"])
            elif type == "can_fix_item":
                perm.can_add_fix = 1
                self.can_fix_item = 5
                self.save(update_fields=["can_fix_item"])
            elif type == "can_add_admin":
                perm.can_add_admin = 1
                self.can_add_admin = 5
                self.save(update_fields=["can_add_admin"])
            elif type == "can_mention":
                perm.can_send_mention = 1
                self.can_mention = 5
                self.save(update_fields=["can_mention"])
            elif type == "can_add_design":
                perm.can_add_design = 1
                self.can_add_design = 5
                self.save(update_fields=["can_add_design"])
            elif type == "can_see_settings":
                perm.can_see_settings = 1
                self.can_see_settings = 5
                self.save(update_fields=["can_see_settings"])
            elif type == "can_see_log":
                perm.can_see_log = 1
                self.can_see_log = 5
                self.save(update_fields=["can_see_log"])
            perm.save()


    def post_exclude_users(self, users, type):
        if type == "can_add_members":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_in_chat=2).update(can_add_in_chat=0)
        elif type == "can_fix_item":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_fix=2).update(can_add_fix=0)
        elif type == "can_add_admin":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_admin=2).update(can_add_admin=0)
        elif type == "can_mention":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_send_mention=2).update(can_send_mention=0)
        elif type == "can_add_design":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_design=2).update(can_add_design=0)
        elif type == "can_see_settings":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_see_settings=2).update(can_see_settings=0)
        elif type == "can_see_log":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_see_log=2).update(can_see_log=0)
        for user_id in users:
            member = self.chat_relation.filter(user_id=user_id).first()
            if ChatPerm.objects.filter(user_id=member.pk).exists():
                perm = ChatPerm.objects.get(user_id=member.pk)
            else:
                perm = ChatPerm.objects.create(user_id=member.pk)
            if type == "can_add_members":
                perm.can_add_in_chat = 2
                self.can_add_members = 4
                self.save(update_fields=["can_add_members"])
            elif type == "can_fix_item":
                perm.can_add_fix = 2
                self.can_fix_item = 4
                self.save(update_fields=["can_fix_item"])
            elif type == "can_add_admin":
                perm.can_add_admin = 2
                self.can_add_admin = 4
                self.save(update_fields=["can_add_admin"])
            elif type == "can_mention":
                perm.can_send_mention = 2
                self.can_mention = 4
                self.save(update_fields=["can_mention"])
            elif type == "can_add_design":
                perm.can_add_design = 2
                self.can_add_design = 4
                self.save(update_fields=["can_add_design"])
            elif type == "can_see_settings":
                perm.can_see_settings = 2
                self.can_see_settings = 4
                self.save(update_fields=["can_see_settings"])
            elif type == "can_see_log":
                perm.can_see_log = 2
                self.can_see_log = 4
                self.save(update_fields=["can_see_log"])
            perm.save()

    def create_image(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.image = photo_input
        self.save(update_fields=['image'])
        new_img = get_thumbnailer(self.image)['avatar'].url.replace('media/', '')
        self.image = new_img
        return self.save(update_fields=['image'])


    def is_user_can_add_members(self, user_id):
        if self.can_add_members == self.ALL_CAN:
            return True
        elif self.can_add_members == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_add_members == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        elif self.can_add_members == self.MEMBERS_BUT and self.get_special_perm_for_user(user_id, 1, 0):
            return True
        elif self.can_add_members == self.SOME_MEMBERS and self.get_special_perm_for_user(user_id, 1, 1):
            return True
        return False
    def is_user_can_fix_item(self, user_id):
        if self.can_fix_item == self.ALL_CAN:
            return True
        elif self.can_fix_item == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_fix_item == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        elif self.can_fix_item == self.MEMBERS_BUT and self.get_special_perm_for_user(user_id, 3, 0):
            return True
        elif self.can_fix_item == self.SOME_MEMBERS and self.get_special_perm_for_user(user_id, 3, 1):
            return True
        return False
    def is_user_can_mention(self, user_id):
        if self.can_mention == self.ALL_CAN:
            return True
        elif self.can_mention == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_mention == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        elif self.can_mention == self.MEMBERS_BUT and self.get_special_perm_for_user(user_id, 4, 0):
            return True
        elif self.can_mention == self.SOME_MEMBERS and self.get_special_perm_for_user(user_id, 4, 1):
            return True
        return False
    def is_user_can_add_admin(self, user_id):
        if self.can_add_admin == self.ALL_CAN:
            return True
        elif self.can_add_admin == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_add_admin == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        return False
    def is_user_can_add_design(self, user_id):
        if self.can_add_design == self.ALL_CAN:
            return True
        elif self.can_add_design == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_add_design == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        elif self.can_add_design == self.MEMBERS_BUT and self.get_special_perm_for_user(user_id, 5, 0):
            return True
        elif self.can_add_design == self.SOME_MEMBERS and self.get_special_perm_for_user(user_id, 5, 1):
            return True
    def is_user_can_see_settings(self, user_id):
        if self.can_see_settings == self.ALL_CAN:
            return True
        elif self.can_see_settings == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_see_settings == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        elif self.can_see_settings == self.MEMBERS_BUT and self.get_special_perm_for_user(user_id, 6, 0):
            return True
        elif self.can_see_settings == self.SOME_MEMBERS and self.get_special_perm_for_user(user_id, 6, 1):
            return True
    def is_user_can_see_log(self, user_id):
        if self.can_see_log == self.ALL_CAN:
            return True
        elif self.can_see_log == self.CREATOR and self.creator.pk == user_id:
            return True
        elif self.can_see_log == self.CREATOR_ADMINS and user_id in self.get_admins_ids():
            return True
        elif self.can_see_log == self.MEMBERS_BUT and self.get_special_perm_for_user(user_id, 7, 0):
            return True
        elif self.can_see_log == self.SOME_MEMBERS and self.get_special_perm_for_user(user_id, 7, 1):
            return True


    def get_special_perm_for_user(self, user_id, type, value):
        """
        type 1 - can_add_members, 3 - can_fix_item, 4 - can_mention, 5 - can_add_design, 6 - can_see_settings, 7 - can_see_log
        value 0 - MEMBERS_BUT(люди, кроме), value 1 - SOME_MEMBERS(некоторые люди)

        Логика такая.
        Если MEMBERS_BUT, то мы проверяем, есть ли запись ChatPerm.
        Если ее нет, тогда правда, если есть и он в поле chat_ie_settings (для типа 1)
        не имеет значение 2 (Не может совершат действия с элементом), тоже правда.

        Если SOME_MEMBERS, то запись должна быть точно, ведь он включающий в список действий.
        Потому если ее нет, то ложь. Если есть и в поле chat_ie_settings (для типа 1)
        стоит значение 1 (может совершать действия с элементом), то правда.
        """
        member = ChatUsers.objects.get(chat_id=self.pk, user_id=user_id)
        if value == 0:
            try:
                ie = member.chat_ie_settings
                if type == 1:
                    return ie.can_add_in_chat != 2
                elif type == 3:
                    return ie.can_add_fix != 2
                elif type == 4:
                    return ie.can_send_mention != 2
                elif type == 5:
                    return ie.can_add_design != 2
                elif type == 6:
                    return ie.can_see_settings != 2
                elif type == 7:
                    return ie.can_see_log != 2
            except ChatPerm.DoesNotExist:
                 return True
        elif value == 1:
            try:
                ie = member.chat_ie_settings
                if type == 1:
                    return ie.can_add_in_chat == 1
                elif type == 3:
                    return ie.can_add_fix == 1
                elif type == 4:
                    return ie.can_send_mention == 1
                elif type == 5:
                    return ie.can_add_design == 1
                elif type == 6:
                    return ie.can_see_settings == 1
                elif type == 7:
                    return ie.can_see_log == 1
            except ChatPerm.DoesNotExist:
                 return False

    def is_private(self):
        return self.type == Chat.PRIVATE
    def is_group(self):
        return self.type == Chat.GROUP
    def is_public(self):
        return self.type == Chat.PUBLIC
    def is_manager(self):
        return self.type == Chat.MANAGER
    def is_open(self):
        return self.type[0] != "_"
    def is_muted(self, user_id):
        chat_user = ChatUsers.objects.get(chat_id=self.pk, user_id=user_id)
        return chat_user.beep()

    def get_members(self):
        from users.models import User
        return User.objects.filter(chat_users__chat__pk=self.pk, chat_users__type="ACT")

    def get_admins(self):
        from users.models import User
        return User.objects.filter(chat_users__chat__pk=self.pk, chat_users__type="ACT", chat_users__is_administrator=True)
    def get_admins_ids(self):
        users = self.get_admins().values('id')
        return [i['id'] for i in users]

    def get_recipients_exclude_creator(self, exclude_creator_pk):
        from users.models import User
        return User.objects.filter(chat_users__chat__id=self.pk, chat_users__type="ACT").exclude(id=exclude_creator_pk)
    def get_recipients(self):
        return ChatUsers.objects.filter(chat_id=self.pk, type="ACT")

    def get_recipients_2(self, exclude_creator_pk):
        return ChatUsers.objects.filter(chat_id=self.pk, type="ACT").exclude(user_id=exclude_creator_pk)

    def get_members_ids(self):
        users = self.get_members().values('id')
        return [i['id'] for i in users]

    def get_recipients_ids(self, exclude_creator_pk):
        users = self.get_recipients_exclude_creator(exclude_creator_pk).values('id')
        return [i['id'] for i in users]

    def get_members_count(self):
        return self.members

    def get_members_count_ru(self):
        count = self.members

        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " участник"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " участника"
        else:
            return str(count) + " участников"

    def get_first_message(self, user_id):
        return self.get_messages(user_id).first()

    def get_attach_photos_ids(self):
        if self.attach:
            ids = []
            for i in self.attach.split(","):
                if i[:3] == "pho":
                    ids.append(int(i[3:]))
            return ids
        return []
    def get_attach_photos(self):
        if self.attach:
            from gallery.models import Photo, PhotoList
            list = []
            for i in self.attach.split(","):
                if i[:3] == "pho":
                    list.append(Photo.objects.get(pk=i[3:]))
                elif i[:3] == "lph":
                    list.append(PhotoList.objects.get(pk=i[3:]))
            return list
        return []
    def get_attach_docs(self):
        if self.attach:
            from docs.models import Doc, DocsList
            list = []
            for i in self.attach.split(","):
                if i[:3] == "doc":
                    list.append(Doc.objects.get(pk=i[3:]))
                elif i[:3] == "ldo":
                    list.append(DocsList.objects.get(pk=i[3:]))
            return list
        return []
    def get_attach_videos_ids(self):
        if self.attach:
            ids = []
            for i in self.attach.split(","):
                if i[:3] == "vid":
                    ids.append(int(i[3:]))
            return ids
        return []
    def get_attach_videos(self):
        if self.attach:
            from video.models import Video, VideoList
            list = []
            for i in self.attach.split(","):
                if i[:3] == "vid":
                    list.append(Video.objects.get(pk=i[3:]))
                elif i[:3] == "lvi":
                    list.append(VideoList.objects.get(pk=i[3:]))
            return list
        return []
    def get_attach_tracks(self):
        if self.attach:
            from music.models import Music, MusicList
            list = []
            for i in self.attach.split(","):
                if i[:3] == "mus":
                    list.append(Music.objects.get(pk=i[3:]))
                elif i[:3] == "lmu":
                    list.append(MusicList.objects.get(pk=i[3:]))
            return list
        return []

    def get_attach_goods_ids(self):
        if self.attach:
            ids = []
            for i in self.attach.split(","):
                if i[:3] == "goo":
                    ids.append(int(i[3:]))
            return ids
        return []
    def get_attach_goods(self):
        if self.attach:
            from goods.models import Good, GoodList
            list = []
            for i in self.attach.split(","):
                if i[:3] == "goo":
                    list.append(Good.objects.get(pk=i[3:]))
                elif i[:3] == "lgo":
                    list.append(GoodList.objects.get(pk=i[3:]))
            return list
        return []
    def get_attach_posts_ids(self):
        if self.attach:
            ids = []
            for i in self.attach.split(","):
                if i[:3] == "pos":
                    ids.append(int(i[3:]))
            return ids
        return []
    def get_attach_posts(self):
        if self.attach:
            from posts.models import Post, PostsList
            list = []
            for i in self.attach.split(","):
                if i[:3] == "pos":
                    list.append(Post.objects.get(pk=i[3:]))
                elif i[:3] == "lpo":
                    list.append(PostsList.objects.get(pk=i[3:]))
            return list
        return []

    def get_unread_count_message(self, user_id):
        count = self.chat_message.filter(unread=True, type__contains="_", message_options__user_id=self.pk, message_options__is_deleted=True).exclude(creator_id=user_id).values("pk").count()
        if count:
            return ''.join(['<span style="font-size: 80%;" class="tab_badge badge-success">', str(count), '</span>'])
        else:
            return ""

    def get_unread_message(self, user_id):
        return self.chat_message.filter(unread=True, type__contains="_").exclude(creator_id=user_id)
    def read_messages(self, user_id):
        self.chat_message.filter(unread=True).exclude(creator_id=user_id).update(unread=False)

    def get_last_message_created(self):
        if self.is_not_empty():
            return self.get_first_message().get_created()
        else:
            return ''

    def get_chat_member(self, user_id):
        members = self.chat_relation.exclude(user_id=user_id)
        return members[0].user
    def get_chat_user(self, user_id):
        try:
            members = self.chat_relation.exclude(user_id=user_id)
            return members[0]
        except:
            member = self.chat_relation.get(user_id=user_id)
            return members
    def get_chat_request_user(self, user_id):
        return self.chat_relation.get(user_id=user_id)

    def get_preview_message(self, user_id):
        first_message, preview_text, is_read, creator_figure, created = self.get_first_message(user_id), '', '', '', ''

        if self.is_have_draft_message(user_id):
            message = self.get_draft_message(user_id)
            preview_text = 'Черновик: ' + message.get_type_text()
        elif not first_message:
            preview_text = "Нет сообщений"
        elif first_message.is_manager():
            created = first_message.get_created()
            if first_message.parent:
                creator = first_message.creator
                message = first_message.parent
                preview_text = creator.get_full_name() + first_message.text + '<span class="underline">' + message.get_text_60() + '</span>'
            else:
                preview_text = first_message.get_text_60()
        else:
            preview_text = first_message.get_text_60()
            if first_message.creator.id == user_id:
                preview_text = 'Вы: ' + first_message.get_type_text()
            else:
                preview_text = first_message.get_type_text()
            if user_id == first_message.creator.pk and first_message.unread:
                is_read = ' bg-light-secondary'
            created = first_message.get_created()

        request_chat_user = self.get_chat_request_user(user_id)

        if self.is_group() or self.is_public():
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            else:
                figure = '<figure><img src="/static/images/group_chat.jpg" style="border-radius:50px;width:50px;" alt="image"></figure>'
            if self.name:
                 chat_name = self.name
            else:
                chat_name = "Групповой чат"
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, request_chat_user.get_beep_icon(), '<small class="float-right text-muted">', created, '</small></h5><p class="mb-0', is_read ,'" style="white-space: nowrap;">', preview_text, '</p></div>'])
            return ''.join(['<div class="media">', figure, media_body, self.get_unread_count_message(user_id), '</div>'])

        elif self.is_private():
            chat_user = self.get_chat_user(user_id)
            member = chat_user.user
            if self.image:
                figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:50px;width:50px;" alt="image"></figure>'])
            elif member.s_avatar:
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
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, request_chat_user.get_beep_icon(), status, '<small class="float-right text-muted">', 'created', '</small></h5><p class="mb-0', is_read ,'" style="white-space: nowrap;">', preview_text, '</p><span class="typed"></span></div>'])
            return ''.join(['<div class="media">', figure, media_body, self.get_unread_count_message(user_id), '</div>'])

    def get_header_chat(self, user_id):
        chat_user = self.get_chat_user(user_id)
        request_chat_user = self.get_chat_request_user(user_id)
        if self.is_user_can_fix_item(user_id):
            fix_btn = '<span tooltip="Закрепить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_fixed" fill="currentColor" viewBox="0 0 24 24"><g><rect fill="none" height="24" width="24"/></g><g><path d="M16,9V4l1,0c0.55,0,1-0.45,1-1v0c0-0.55-0.45-1-1-1H7C6.45,2,6,2.45,6,3v0 c0,0.55,0.45,1,1,1l1,0v5c0,1.66-1.34,3-3,3h0v2h5.97v7l1,1l1-1v-7H19v-2h0C17.34,12,16,10.66,16,9z" fill-rule="evenodd"/></g></svg></span>'
        else:
            fix_btn = ""
        buttons = '<span class="console_btn_other btn_default" style="display:none;padding-top:5px"><span class="one_message"><span tooltip="Ответить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_reply" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z"/></svg></span><span tooltip="Пожаловаться" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_claim" viewBox="0 0 24 24" fill="currentColor"><path d="M11 15h2v2h-2v-2zm0-8h2v6h-2V7zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/></svg></span><span tooltip="Редактировать" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_edit" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg></span>' + fix_btn + '</span><span tooltip="Удалить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_delete" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4h-3.5z"/></svg></span><span tooltip="Переслать" flow="up"><svg class="svg_default_30 pointer u_message_transfer" viewBox="0 0 24 24" fill="currentColor"><path d="m0 0h24v24h-24z" fill="none"/><path fill="currentColor" d="m12.1 7.87v-3.47a1.32 1.32 0 0 1 2.17-1l8.94 7.6a1.32 1.32 0 0 1 .15 1.86l-.15.15-8.94 7.6a1.32 1.32 0 0 1 -2.17-1v-3.45c-4.68.11-8 1.09-9.89 2.87a1.15 1.15 0 0 1 -1.9-1.11c1.53-6.36 5.51-9.76 11.79-10.05zm1.8-2.42v4.2h-.9c-5.3 0-8.72 2.25-10.39 6.86 2.45-1.45 5.92-2.16 10.39-2.16h.9v4.2l7.71-6.55z" /></svg></span><span flow="up"><svg class="svg_default_30 ml-1 toggle_messages_favourite pointer" fill="currentColor" enable-background="new 0 0 24 24" viewBox="0 0 24 24"></svg></span></span>'

        if self.is_public():
            chat_name, dop_drops, target_display = "Групповой чат", '', '<span class="u_chat_info pointer type_display small" style="position:absolute;top: 21px;">' + self.get_members_count_ru() + '</span>'
            if self.is_user_can_add_members(user_id):
                dop_drops += '<a class="dropdown-item u_add_members_in_chat pointer">Добавить друзей</a>'
            dop_drops += '<a class="dropdown-item user_exit_in_user_chat pointer">Выйти из чата</a>'
        elif self.is_group():
            chat_name, dop_drops, target_display = "Публичный чат", '', '<span class="u_chat_info pointer type_display small" style="position:absolute;top: 21px;">' + self.get_members_count_ru() + '</span>'
            if self.is_user_can_add_members(user_id):
                dop_drops += '<a class="dropdown-item u_add_members_in_chat pointer">Добавить друзей</a>'
            dop_drops += '<a class="dropdown-item user_exit_in_user_chat pointer">Выйти из чата</a>'
        elif self.is_private():
            member = chat_user.user
            chat_name, dop_drops, target_display = '<a href="' + member.get_link() + '" target="_blank">' + member.get_full_name() + '</a>', '<a class="dropdown-item add_member_in_chat pointer">Добавить в чат</a><a class="dropdown-item u_delete_chat pointer">Удалить чат</a>', '<span class="type_display small" style="position:absolute;top: 21px;">' + member.get_online_status() + '</span>'
        elif self.is_manager():
            chat_name, dop_drops, target_display = "Служебный чат", '', '<span class="type_display small" style="position:absolute;top: 21px;">Категория такая-то</span>'
            dop_drops += '<a class="dropdown-item u_clean_chat_messages pointer">Выйти из чата</a>'
        elif self.is_support():
            chat_name = "Чат техподдержки"
            dop_drops += '<a class="dropdown-item u_clean_chat_messages pointer">Выйти из чата</a>'
            target_display = '<span class="type_display small" style="position:absolute;top: 21px;">Агент поддержки такой-то</span>'
        if not self.is_muted(user_id):
            muted_drop = '<span><a class="dropdown-item on_full_chat_notify pointer">Вкл. уведомления</a></span>'
        else:
            muted_drop = '<span><a class="dropdown-item off_full_chat_notify pointer">Откл. уведомления</a></span>'

        if self.name:
             chat_name = self.name
        media_body = ''.join(['<div class="media-body" style="overflow: inherit;padding-top: 3px;"><h5 class="time-title mb-1"><span class="u_chat_info pointer">', chat_name, '</span><span class="notify_box">', request_chat_user.get_beep_icon(), '</h5><span class="mt-1 mb-2 target_display">', target_display, buttons, '</span></div>'])
        dropdown = ''.join(['<div class="dropdown d-inline-block"><a style="cursor:pointer" class="icon-circle icon-30 btn_default drop"><svg class="svg_info" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 29px; width: 100%;"><a class="dropdown-item chat_search pointer">Поиск сообщений</a><a class="dropdown-item show_attach_files pointer">Показать вложения</a>', muted_drop, dop_drops,'<a class="dropdown-item u_clean_chat_messages pointer">Очистить историю</a></div></div>'])
        return ''.join([media_body, dropdown])

    def is_not_empty(self, user_pk):
        return self.chat_message.exclude(type__contains="_").exists()

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

    def get_draft_message(self, user_id):
        return self.chat_message.filter(chat_id=self.pk, creator_id=user_id, type=Message.DRAFT).first()

    def is_have_draft_message(self, user_id):
        if self.chat_message.filter(chat_id=self.pk, creator_id=user_id, type=Message.DRAFT).exists():
            message = self.chat_message.filter(chat_id=self.pk, creator_id=user_id, type=Message.DRAFT).first()
            if message.text or message.attach or message.is_have_transfer():
                return True
        return False
    def get_first_fix_message(self):
        if Message.objects.filter(chat_id=self.id, type__contains="FIX").exists():
            return self.chat_message.filter(chat_id=self.id, type__contains="FIX").first()

    def get_fixed_messages(self):
        return self.chat_message.filter(chat_id=self.id, type__contains="FIX")

    def get_fix_message_count(self):
        if self.chat_message.filter(chat_id=self.id, type__contains="FIX").exists():
            return self.chat_message.filter(chat_id=self.id, type__contains="FIX").values("pk").count()
        else:
            return 0

    def get_fix_message_count_ru(self):
        count = self.get_fix_message_count()

        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " сообщение"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " сообщения"
        else:
            return str(count) + " сообщений"

    def delete_member(self, user, creator):
        from datetime import datetime

        if creator.is_women():
            var = "исключила"
        else:
            var = "исключил"
        ChatUsers.delete_member(user=user, chat=self)
        text = '<a target="_blank" href="' + creator.get_link() + '">' + creator.get_full_name() + '</a>&nbsp;' + var + '&nbsp;<a target="_blank" href="' + user.get_link() + '">' + user.get_full_name_genitive() + '</a>'
        info_message = Message.objects.create(chat_id=self.id,creator_id=creator.id,type=Message.MANAGER,text=text)
        for recipient in self.get_recipients_2(creator.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        self.created = datetime.now()
        self.save(update_fields=["created"])
        self.chat_message.filter(chat_id=self.pk, creator_id=user.pk, type=Message.DRAFT).delete()
        return info_message

    def exit_member(self, user):
        from datetime import datetime

        if user.is_women():
            var = "вышла из чата"
        else:
            var = "вышел из чата"
        ChatUsers.exit_member(user=user, chat=self)
        text = '<a target="_blank" href="' + user.get_link() + '">' + user.get_full_name() + '</a>&nbsp;' + var
        info_message = Message.objects.create(chat_id=self.id,creator_id=user.id,type=Message.MANAGER,text=text)
        for recipient in self.get_recipients_2(user.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        self.created = datetime.now()
        self.save(update_fields=["created"])
        self.chat_message.filter(chat_id=self.pk, creator_id=user.pk, type=Message.DRAFT).delete()
        return info_message

    def invite_users_in_chat(self, users_ids, creator):
        from users.models import User
        from datetime import datetime

        if creator.is_women():
            var = "пригласила"
        else:
            var = "пригласил"
        users = User.objects.filter(id__in=users_ids)
        info_messages = []
        for user in users:
            if not ChatUsers.objects.filter(user=user, chat=self).exclude(type="DEL").exists():
                member = ChatUsers.create_membership(user=user, chat=self)
                if member:
                    text = '<a target="_blank" href="' + creator.get_link() + '">' + creator.get_full_name() + '</a>&nbsp;' + var + '&nbsp;<a target="_blank" href="' + user.get_link() + '">' + user.get_full_name_genitive() + '</a>'
                    info_message = Message.objects.create(chat_id=self.id,creator_id=creator.id,type=Message.MANAGER,text=text)
                    info_messages.append(info_message)
                    for recipient in self.get_recipients_2(creator.pk):
                        info_message.create_socket(recipient.user.pk, recipient.beep())
        self.created = datetime.now()
        self.save(update_fields=["created"])
        return info_messages

    def edit_chat(self, name, image, description):
        self.name = name
        self.description = description
        if image:
            self.create_image(image)
        self.save()
        return self

    def get_add_in_chat_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_in_chat=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_add_in_chat_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_in_chat=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_can_fix_item_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_fix=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_fix_item_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_fix=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_can_mention_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_send_mention=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_mention_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_send_mention=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_can_add_admin_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_admin=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_add_admin_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_admin=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_can_add_design_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_design=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_add_design_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_design=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_can_see_settings_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_see_settings=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_see_settings_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_see_settings=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_can_see_log_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_see_log=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_see_log_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_see_log=2).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])

    def get_messages(self, user_id):
        query = Q()
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(message_options__user_id=user_id, message_options__is_deleted=True), Q.AND)
        return self.chat_message.filter(query)
    def is_not_empty(self, user_id):
        query = Q()
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(message_options__user_id=user_id, message_options__is_deleted=True), Q.AND)
        return self.chat_message.filter(query).exists()

    def get_messages_uuids(self, user_id):
        query = Q()
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(message_options__user_id=user_id), Q.AND)
        list = self.chat_message.filter(query).values("uuid")
        return [i['uuid'] for i in list]


class ChatUsers(models.Model):
    ACTIVE, EXITED, DELETED = "ACT", "EXI", "DEL"
    TYPE = (
        (ACTIVE, 'Действующий'),(EXITED, 'Вышедший'),(DELETED, 'Уделенный'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='chat_users', null=False, blank=False, verbose_name="Члены сообщества")
    chat = models.ForeignKey(Chat, db_index=False, on_delete=models.CASCADE, related_name='chat_relation', verbose_name="Чат")
    is_administrator = models.BooleanField(default=False, verbose_name="Это администратор")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    no_disturb = models.DateTimeField(blank=True, null=True, verbose_name='Не беспокоить до...')
    type = models.CharField(max_length=3, choices=TYPE, default=ACTIVE, verbose_name="Тип участника")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        unique_together = (('user', 'chat'),)
        indexes = [
            models.Index(fields=['chat', 'user']),
            models.Index(fields=['chat', 'user', 'is_administrator'])
            ]
        verbose_name = 'участник беседы'
        verbose_name_plural = 'участники бесед'

    @classmethod
    def create_membership(cls, user, chat, is_administrator=False):
        # создание участника по приглашению
        if cls.objects.filter(user=user, chat=chat).exists():
            member = cls.objects.get(user=user, chat=chat)
            if member.type == ChatUsers.DELETED:
                # если он сам не вышел из беседы
                member.type = ChatUsers.ACTIVE
                member.save(update_fields=["type"])
                chat.members = chat.members + 1
                chat.save(update_fields=["members"])
                return member
            else:
                pass
        else:
            membership = cls.objects.create(user=user, chat=chat, is_administrator=is_administrator)
            chat.members = chat.members + 1
            chat.save(update_fields=["members"])
            return membership

    def exit_member(user, chat):
        # Человек сам выходит из группового чата и больше приглашать его в этот чат нельзя
        if ChatUsers.objects.filter(user=user, chat=chat).exists():
            member = ChatUsers.objects.get(user=user, chat=chat)
            member.type = "EXI"
            member.save(update_fields=["type"])
            members = chat.members
            if members > 0:
                chat.members = chat.members - 1
                chat.save(update_fields=["members"])

    def delete_member(user, chat):
        # Человека удаляют из группового чата и он может вернуться только по приглашению админов
        if ChatUsers.objects.filter(user=user, chat=chat).exists():
            member = ChatUsers.objects.get(user=user, chat=chat)
            member.type = "DEL"
            member.save(update_fields=["type"])
            members = chat.members
            if members > 0:
                chat.members = chat.members - 1
                chat.save(update_fields=["members"])

    def beep(self):
        if not self.no_disturb:
            return True
        else:
            from datetime import datetime
            return self.no_disturb < datetime.now()

    def get_beep_icon(self):
        if not self.beep():
            return ' <svg style="width: 15px;" enable-background="new 0 0 24 24" height="15px" viewBox="0 0 24 24" width="17px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M4.34 2.93L2.93 4.34 7.29 8.7 7 9H3v6h4l5 5v-6.59l4.18 4.18c-.65.49-1.38.88-2.18 1.11v2.06c1.34-.3 2.57-.92 3.61-1.75l2.05 2.05 1.41-1.41L4.34 2.93zM10 15.17L7.83 13H5v-2h2.83l.88-.88L10 11.41v3.76zM19 12c0 .82-.15 1.61-.41 2.34l1.53 1.53c.56-1.17.88-2.48.88-3.87 0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zm-7-8l-1.88 1.88L12 7.76zm4.5 8c0-1.77-1.02-3.29-2.5-4.03v1.79l2.48 2.48c.01-.08.02-.16.02-.24z"/></svg>'
        else:
            return ''


class ChatPerm(models.Model):
    """ связь с таблицей участников беседы. Появляется после ее инициирования, когда участник
        получит какое либо исключение или включение для какой-либо категории.
        1. NO_VALUE - неактивное значение.
        2. YES_ITEM - может соверщать описанные действия
        3. NO_ITEM - не может соверщать описанные действия
    """
    NO_VALUE, YES_ITEM, NO_ITEM = 0, 1, 2
    ITEM = (
        (NO_VALUE, 'Не активно'),
        (YES_ITEM, 'Может иметь действия с элементом'),
        (NO_ITEM, 'Не может иметь действия с элементом'),
    )

    user = models.OneToOneField(ChatUsers, null=True, blank=True, on_delete=models.CASCADE, related_name='chat_ie_settings', verbose_name="Друг")

    can_add_in_chat = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет в беседы")
    can_add_fix = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто закрепляет сообщения")
    can_send_mention = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто отправляет массовые упоминания")
    can_add_admin = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет админов и работает с ними")
    can_add_design = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто меняет дизайн")
    can_see_settings = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит настройки")
    can_see_log = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит журнал действий")

    class Meta:
        verbose_name = 'Исключения/Включения участника беседы'
        verbose_name_plural = 'Исключения/Включения участников беседы'
        index_together = [('id', 'user'),]


class Message(models.Model):
    PUBLISHED, EDITED, DELETED, CLOSED, DRAFT, MANAGER, PUBLISHED_FIXED, EDITED_FIXED = 'PUB','EDI','_DEL','_CLO','_DRA','MAN','PFIX','EFIX'
    DELETED_EDITED, CLOSED_EDITED, DELETED_PUBLISHED_FIXED, CLOSED_PUBLISHED_FIXED, DELETED_EDITED_FIXED, CLOSED_EDITED_FIXED = '_DELE','_CLOE', '_DELPF','_CLOPF', '_DELEF','_CLOEF'
    TYPE = (
        (PUBLISHED_FIXED, 'Закреп опубл'),(EDITED_FIXED, 'Закреп измен'),(MANAGER, 'Служебное'),(PUBLISHED, 'Опубл'),(DELETED, 'Удалено'),(EDITED, 'Изменено'),(CLOSED, 'Закрыто модератором'),(DRAFT, 'Черновик'),
        (DELETED_EDITED_FIXED, 'Удал измен закреп'),(DELETED_PUBLISHED_FIXED, 'Удал опубл закреп'),(CLOSED_EDITED_FIXED, 'Закр измен закреп'),(CLOSED_PUBLISHED_FIXED, 'Закр опубл закреп'),(CLOSED_PUBLISHED_FIXED, 'Закр опубл закреп'),(DELETED_EDITED, 'Удал измен'),(CLOSED_EDITED, 'Закр измен'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_creator', verbose_name="Создатель", null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_message")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_thread")
    sticker = models.ForeignKey(Stickers, blank=True, null=True, on_delete=models.CASCADE, related_name="+")
    repost = models.ForeignKey("posts.Post", on_delete=models.CASCADE, null=True, blank=True, related_name='post_message')
    #transfer = models.ManyToManyField("self", blank=True, related_name='+')

    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=10000, blank=True)
    unread = models.BooleanField(default=True, db_index=True, verbose_name="Не прочитано")
    type = models.CharField(choices=TYPE, default=PUBLISHED, max_length=6, verbose_name="Статус сообщения")
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    voice = models.FileField(blank=True, upload_to=upload_to_chat_directory, verbose_name="Голосовое сообщение")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.text

    def get_draft_transfers_block(self):
        transfers = self.get_transfers()
        count = transfers.count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            text = str(count) + " сообщение"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            text = str(count) + " сообщения"
        else:
            text = str(count) + " сообщений"
        if count > 1:
            text_2 = "Пересланные сообщения"
        else:
            text_2 = "Пересланное сообщение"
        inputs = ""
        for i in transfers:
            inputs += '<input type="hidden" name="transfer" value="' + str(i.uuid) + '" class="transfer">'
        return '<div><p>' + text_2 + '</p><div style="position:relative;padding-bottom:7px"><div><span class="pointer underline">' + text + '</span><span class="remove_parent_block pointer message_form_parent_block">x</span></div></div>' + inputs + '</div>'

    def is_edited(self):
        return self.type == "EDI"
    def is_manager(self):
        return self.type == Message.MANAGER
    def is_fixed(self):
        return self.type == Message.PUBLISHED_FIXED or self.type == Message.EDITED_FIXED
    def is_favourite(self, user_id):
        return MessageOptions.objects.filter(message_id=self.pk,user_id=user_id, is_favourite=True).exists()

    def is_have_transfer(self):
        return MessageTransfers.objects.filter(message_id=self.pk).exists()

    def get_transfers_ids(self):
        values = MessageTransfers.objects.filter(message_id=self.pk).values("transfer_id")
        return [i['transfer_id'] for i in values]
    def get_transfers(self):
        return Message.objects.filter(uuid__in=self.get_transfers_ids()).exclude(type__contains="_")

    def get_count_attach(self):
        if self.attach:
            length = self.attach.split(",")
            return "files_" + str(len(length))
        else:
            return "files_0"

    def get_parent_message(self):
        if not self.parent:
            return '<div class="media p-1 pag">Нет ответа!</div>'
        parent = self.parent
        if parent.voice:
            preview = "Голосовое сообщение"
        if parent.sticker:
            preview = "Наклейка"
        if parent.attach:
            preview = "Вложения"
        else:
            preview = parent.text[:80]
        user = parent.creator

        return '<div class="media p-1" data-uuid="' + str(parent.uuid) + '" style="border-left: 1px solid rgba(0, 0, 0, 0.7)"><span style="padding-top: 6px;"><a href="' + user.get_link() + '" class="ajax">' + user.get_s_avatar() + '</a></span><div class="media-body" style="line-height: 1em;padding-left: 3px;"><p class="time-title mb-0"><a href="' + user.get_link()  + '" class="ajax">' + user.get_full_name() + '</a></p><small class="text-muted">' + parent.get_created() + '</small><p class="text">' + preview + '</p></div></div>'

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def get_creator(self):
        return self.creator.user
    def get_recipient(self):
        return self.recipient.user

    def get_reseiver_ids(self):
        return self.chat.get_members_ids()

    def create_socket(self, recipient_id, beep_on):
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'message',
            'message_id': str(self.uuid),
            'chat_id': str(self.chat.pk),
            'recipient_id': str(recipient_id),
            'name': "u_message_create",
            'beep': beep_on,
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

    def get_format_attach(value):
        _attach = str(value)
        return _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "").replace("<div class='attach_container'></div>", "")

    def get_format_text(text):
        from common.processing_2 import get_text_processing
        if text:
            return get_text_processing(text, True)
        else:
            return ""

    def get_or_create_chat_and_send_message(creator, user, repost, text, attach, voice, sticker):
        from datetime import datetime

        chat_list, current_chat = creator.get_all_chats(), None
        _text = Message.get_format_text(text)
        for chat in chat_list:
            if user.pk in chat.get_members_ids() and chat.is_private():
                current_chat = chat
        if not current_chat:
            # участники нового чата не имеют административных прав. Они им не нужны.
            # ведь админы могут удалять любые сообщения чата. В приватном же чате - только
            # свои чтоб могли.
            current_chat = Chat.objects.create(creator=creator, type=Chat.PRIVATE)
            ChatUsers.objects.create(user=creator, chat=current_chat)
            ChatUsers.objects.create(user=user, chat=current_chat)

        if voice:
            message = Message.objects.create(chat=current_chat, creator=creator, repost=repost, voice=voice)
        elif sticker:
            message = Message.objects.create(chat=current_chat, creator=creator, repost=repost, sticker_id=sticker)
            from common.model.other import UserPopulateStickers
            UserPopulateStickers.get_plus_or_create(user_pk=creator.pk, sticker_pk=sticker)
        else:
            message = Message.objects.create(chat=current_chat, creator=creator, repost=repost, text=_text, attach=Message.get_format_attach(attach))
        current_chat.created = datetime.now()
        if attach:
            if current_chat.attach:
                current_chat.attach = current_chat.attach + ", " + attach
            else:
                current_chat.attach = attach
            current_chat.save(update_fields=["created", "attach"])
        else:
            current_chat.save(update_fields=["created"])
        for recipient in current_chat.get_recipients_2(creator.pk):
            message.create_socket(recipient.user.pk, recipient.beep())

    def get_or_create_support_chat_and_send_message(creator, user, repost, text, attach, voice, sticker):
        from datetime import datetime

        _text = Message.get_format_text(text)
        chat = creator.get_or_create_support_chat_pk()

        if voice:
            message = Message.objects.create(chat=chat, creator=creator, voice=voice)
        else:
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, text=_text, attach=Message.get_format_attach(attach))
        chat.created = datetime.now()
        if attach:
            if chat.attach:
                chat.attach = chat.attach + ", " + attach
            else:
                chat.attach = attach
            chat.save(update_fields=["created", "attach"])
        else:
            chat.save(update_fields=["created"])
        for recipient in chat.get_recipients_2(creator.pk):
            message.create_socket(recipient.user.pk, recipient.beep())

    def get_or_create_manager_chat_and_send_message(creator_pk, text, attach, voice):
        # создаем массовую расслылку сообщений
        from users.models import User

        users = User.objects.filter(type__contains="_")
        _text = Message.get_format_text(text)
        _attach = Message.get_format_attach(attach)
        objs = [
            Message(
                    chat_id = user.get_or_create_manager_chat_pk(),
                    creator_id = creator_pk,
                    voice = voice,
                    text = _text,
                    attach = _attach,
                )
                for user in users
            ]
        Message.objects.bulk_create(objs)

        for user in users:
            Message.create_socket(user.pk, recipient.beep())

    def create_chat_append_members_and_send_message(creator, users_ids, text, attach, voice, sticker):
        # Создаем коллективный чат и добавляем туда всех пользователей из полученного списка
        from datetime import datetime

        chat = Chat.objects.create(creator=creator, type=Chat.GROUP)
        _text = Message.get_format_text(text)

        if voice:
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, voice=voice)
        elif sticker:
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, sticker_id=sticker)
            from common.model.other import UserPopulateStickers
            UserPopulateStickers.get_plus_or_create(user_pk=creator.pk, sticker_pk=sticker)
        else:
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, text=_text, attach=Message.get_format_attach(attach))

        for recipient in chat.get_recipients_2(creator.pk):
            message.create_socket(recipient.user.pk, recipient.beep())
        if attach:
            current_chat.attach = attach
            current_chat.save(update_fields=["attach"])

    def send_message(chat, creator, repost, parent, text, attach, voice, sticker, transfer):
        # программа для отсылки сообщения в чате
        from datetime import datetime

        _text = Message.get_format_text(text)

        if parent:
            parent_id = parent
        else:
            parent_id = None
        if voice:
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, voice=voice, parent_id=parent_id)
        elif sticker:
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, sticker_id=sticker, parent_id=parent_id)
            from common.model.other import UserPopulateStickers
            UserPopulateStickers.get_plus_or_create(user_pk=creator.pk, sticker_pk=sticker)
        else:
            if text:
                import re
                ids = re.findall(r'data-pk="(?P<pk>\d+)"', text)
                if ids:
                    from common.model.other import UserPopulateSmiles
                    for id in ids:
                        UserPopulateSmiles.get_plus_or_create(user_pk=creator.pk, smile_pk=id)
            message = Message.objects.create(chat=chat, creator=creator, repost=repost, text=_text, attach=Message.get_format_attach(attach), parent_id=parent_id)
            if transfer:
                for i in transfer:
                    MessageTransfers.objects.create(message_id=message.uuid, transfer_id=i)
            if chat.is_have_draft_message(creator.pk):
                _message = chat.get_draft_message(creator.pk)
                _message.text = ""
                _message.attach = ""
                _message.parent_id = None
                MessageTransfers.objects.filter(message_id=_message.uuid).delete()
                _message.save(update_fields=["text","attach","parent_id"])

        for recipient in chat.get_recipients_2(creator.pk):
            message.create_socket(recipient.user.pk, recipient.beep())

        chat.created = datetime.now()
        chat.save(update_fields=["created"])
        if attach:
            _attach = Message.get_format_attach(attach)
            if chat.attach:
                chat.attach = chat.attach + "," + _attach
            else:
                chat.attach = _attach
            chat.save(update_fields=["created", "attach"])
        else:
            chat.save(update_fields=["created"])
        for recipient in chat.get_recipients_2(creator.pk):
            message.create_socket(recipient.user.pk, recipient.beep())
        return message

    def save_draft_message(chat, creator, parent, text, attach, transfer):
        # программа для сохранения черновика сообщения в чате, а также посылания сокета
        # всем участникам чата, что создатель черновика набирает сообщение
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        if parent:
            parent_id = parent
        else:
            parent_id = None

        if text:
            import re
            ids = re.findall(r'data-pk="(?P<pk>\d+)"', text)
            if ids:
                from common.model.other import UserPopulateSmiles
                for id in ids:
                    UserPopulateSmiles.get_plus_or_create(user_pk=creator.pk, smile_pk=id)

        if chat.is_have_draft_message(creator.pk):
            message = chat.get_draft_message(creator.pk)
            message.text = text
            message.attach = Message.get_format_attach(attach)
            message.parent_id = parent_id
            message.save(update_fields=["text","attach","parent_id"])

        else:
            message = Message.objects.create(chat=chat, creator_id=creator.pk, text=text, attach=Message.get_format_attach(attach), parent_id=parent_id, type=Message.DRAFT)
        MessageTransfers.objects.filter(message_id=message.uuid).delete()
        if transfer:
            for i in transfer:
                MessageTransfers.objects.create(message_id=message.uuid, transfer_id=i)

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'message',
            'chat_id': chat.pk,
            'recipient_id': str(creator.pk),
            'name': "u_message_typed",
            'user_name': creator.first_name,
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

    def fixed_message_for_user_chat(self, creator):
        if "FIX" in self.type:
            return
        from datetime import datetime

        if self.type == Message.PUBLISHED:
            self.type = Message.PUBLISHED_FIXED
        elif self.type == Message.EDITED:
            self.type = Message.EDITED_FIXED
        self.save(update_fields=["type"])

        if creator.is_women():
            var = " закрепила"
        else:
            var = " закрепил"
        text = var + " сообщение "
        info_message = Message.objects.create(chat_id=self.chat.id,creator_id=creator.id,type=Message.MANAGER,text=text,parent=self)
        for recipient in self.chat.get_recipients_2(creator.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        self.chat.created = datetime.now()
        self.chat.save(update_fields=["created"])
        return info_message

    def unfixed_message_for_user_chat(self, creator):
        if not "FIX" in self.type:
            return

        from datetime import datetime
        if self.type == Message.PUBLISHED_FIXED:
            self.type = Message.PUBLISHED
        elif self.type == Message.EDITED_FIXED:
            self.type = Message.EDITED
        self.save(update_fields=["type"])
        if creator.is_women():
            var = " открепила"
        else:
            var = " открепил"
        text = var + " сообщение "
        info_message = Message.objects.create(chat_id=self.chat.id,creator_id=creator.id,type=Message.MANAGER,text=text,parent=self)
        for recipient in self.chat.get_recipients_2(creator.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        self.chat.created = datetime.now()
        self.chat.save(update_fields=["created"])
        return info_message

    def edit_message(self, text, attach):
        from common.processing.message import get_edit_message_processing

        MessageVersion.objects.create(message=self, text=self.text, attach=self.attach.replace("<div class='attach_container'></div>", ""))
        if self.type == Message.PUBLISHED:
            self.type = Message.EDITED
        elif self.type == Message.PUBLISHED_FIXED:
            self.type = Message.EDITED_FIXED
        self.attach = self.get_attach(attach)
        self.text = text
        get_edit_message_processing(self)
        self.save()
        return self

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_text_60(self):
        import re
        count, link_text = 60, None
        images = re.findall(r'<img.*?>', self.text)
        links = re.findall(r'<a.*?>', self.text)
        if images:
            for image in images:
                count += (len(image) -1)
        if links:
            _loop, _exlude, this, next = [self.text], [], -1, 0
            for link in links:
                _loop[next] = '<b class="i_link">' + re.sub('<[A-Za-z\/][^>]*>', '', _loop[this])[:50] + "</b>"
                count += (len(_loop[next]) -1)
            link_text = _loop[next]
        if link_text:
            return link_text[:count].replace("<br>", "  ")
        else:
            return self.text[:count].replace("<br>", "  ")

    def get_type_text(self):
        if self.is_have_transfer():
            if len(self.get_transfers_ids()) > 1:
                return "<b class='i_link'>Пересланные сообщения</b>"
            else:
                return "<b class='i_link'>Пересланное сообщение</b>"
        elif self.parent:
            if self.is_manager():
                creator, message = self.creator, self.parent
                return "<b class='i_link'>" + creator.get_full_name() + self.text + '<span class="underline">' + message.get_text_60() + '</span></b>'
            else:
                return "<b class='i_link'>Ответ на сообщение</b>"
        elif self.sticker:
            return "<b class='i_link'>Стикер</b>"
        elif self.voice:
            return "<b class='i_link'>Голосовое сообщение</b>"
        elif self.attach and self.text:
            return "<b class='i_link'>Текст и вложения</b>"
        elif self.attach and not self.text:
            return "<b class='i_link'>Вложения</b>"
        elif self.text:
            return self.get_text_60()
        else:
            return "Нет текста!"

    def get_preview_text(self):
        if self.is_manager():
            creator = self.creator
            message = self.parent
            return creator.get_full_name() + self.text + '<span class="underline">' + message.get_text_60() + '</span>'
        else:
            return self.get_type_text()

    def get_manager_text(self):
        if self.parent:
            message = self.parent
            text = message.get_type_text()
            return '<i><a target="_blank" href="' + self.creator.get_link() + '">' + self.creator.get_full_name() + '</a><span>' + self.text + '</span><a class="pointer show_selected_fix_message underline">' + text + '</a>' + '</i>'
        else:
            return self.text

    def is_repost(self):
        return self.repost

    def is_photo_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.PHOTO_REPOST)
    def get_photo_repost(self):
        photo = self.repost.parent.item_photo.filter(is_deleted=False)[0]
        return photo
    def is_photo_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.PHOTO_LIST_REPOST)
    def get_photo_list_repost(self):
        return self.repost.parent.post_list.filter(is_deleted=False)[0]

    def is_music_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.MUSIC_REPOST)
    def is_music_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.MUSIC_LIST_REPOST)
    def get_playlist_repost(self):
        playlist = self.repost.parent.post_musiclist.exclude(type__contains="_")[0]
        return playlist
    def get_music_repost(self):
        music = self.repost.parent.item_music.exclude(type__contains="_")[0]
        return music

    def is_good_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.GOOD_REPOST)
    def is_good_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.GOOD_LIST_REPOST)
    def get_good_repost(self):
        return self.repost.item_good.exclude(type__contains="_")[0]
    def get_good_list_repost(self):
        return self.repost.parent.post_good_list.exclude(type__contains="_")[0]

    def is_doc_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.DOC_REPOST)
    def is_doc_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.DOC_LIST_REPOST)
    def get_doc_list_repost(self):
        return self.repost.parent.post_doclist.exclude(type__contains="_")[0]
    def get_doc_repost(self):
        return self.repost.parent.item_doc.exclude(type__contains="_")[0]

    def is_video_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.VIDEO_REPOST)
    def is_video_list_repost(self):
        from posts.models import Post
        return try_except(self.repost.type == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        return self.repost.parent.post_video_list.exclude(type__contains="_")[0]

    def get_u_message_parent(self, user):
        from common.attach.message_attach import get_u_message_parent
        return get_u_message_parent(self.parent, user)

    def get_c_message_parent(self, user):
        from common.attach.message_attach import get_c_message_parent
        return get_c_message_parent(self.parent, user)

    def get_attach(self, user):
        from common.attach.message_attach import get_message_attach
        return get_message_attach(self, user)

    def get_edit_attach(self, user):
        from common.attach.message_attach import get_message_edit
        return get_message_edit(self, user)

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "vid" in self.attach:
            query = []
            from video.models import Video
            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)

    def add_favourite_messages(user_id, list):
        for uuid in list.split(","):
            MessageOptions.objects.create(message_id=uuid,user_id=user_id,is_favourite=True)

    def remove_favourite_messages(user_id, list):
        for uuid in list.split(","):
            MessageOptions.objects.filter(message_id=uuid,user_id=user_id,is_favourite=True).delete()

    def delete_item(self, user_id, community):
        if self.creator_id == user_id or user_id in self.chat.get_admins_ids():
            if self.type == "PUB":
                self.type = Message.DELETED
            elif self.type == "EDI":
                self.type = Message.DELETED_EDITED
            elif self.type == "PFIX":
                self.type = Message.DELETED_PUBLISHED_FIXED
            elif self.type == "EFIX":
                self.type = Message.DELETED_EDITED_FIXED
            self.save(update_fields=['type'])
        else:
            MessageOptions.objects.create(message_id=self.pk,user_id=user_id, is_deleted=True)

    def restore_item(self, user_id, community):
        if self.creator_id == user_id:
            if self.type == "_DEL":
                self.type = Message.PUBLISHED
            elif self.type == "_DELE":
                self.type = Message.EDITED
            elif self.type == "_DELPF":
                self.type = Message.PUBLISHED_FIXED
            elif self.type == "_DELEF":
                self.type = Message.EDITED_FIXED
            self.save(update_fields=['type'])
        else:
            if MessageOptions.objects.filter(message_id=self.pk,user_id=user_id).exists():
                MessageOptions.objects.filter(message_id=self.pk,user_id=user_id).delete()

    def close_item(self, community):
        if self.type == "PUB":
            self.type = Message.CLOSED
        elif self.type == "EDI":
            self.type = Message.CLOSED_EDITED
        elif self.type == "PFIX":
            self.type = Message.CLOSED_PUBLISHED_FIXED
        elif self.type == "EFIX":
            self.type = Message.CLOSED_EDITED_FIXED
        self.save(update_fields=['type'])
    def abort_close_item(self, community):
        if self.type == "_CLO":
            self.type = Message.PUBLISHED
        elif self.type == "_CLOE":
            self.type = Message.EDITED
        elif self.type == "_CLOPF":
            self.type = Message.PUBLISHED_FIXED
        elif self.type == "_CLOEF":
            self.type = Message.EDITED_FIXED
        self.save(update_fields=['type'])


class MessageVersion(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_version")
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000, blank=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    transfer = models.ManyToManyField("self", blank=True, related_name='+')

    class Meta:
        verbose_name = "Копия сообщения перед изменением"
        verbose_name_plural = "Копии сообщений перед изменением"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.text


class MessageOptions(models.Model):
    message = models.ForeignKey(Message, db_index=False, on_delete=models.CASCADE, related_name="message_options")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='message_options_user', verbose_name="Пользователь-инициатор исключения")
    is_deleted = models.BooleanField(default=False, verbose_name="Это сообщение пользователь удалил")
    is_favourite = models.BooleanField(default=False, verbose_name="Это сообщение пользователь поместил в избранное")

    class Meta:
        unique_together = ('message', 'user',)
        indexes = [models.Index(fields=['message', 'user']),]


class MessageTransfers(models.Model):
    message = models.ForeignKey(Message, db_index=False, on_delete=models.CASCADE, related_name="+", verbose_name="Сообщение, в котором пересылают")
    transfer = models.ForeignKey(Message, db_index=False, on_delete=models.CASCADE, related_name='+', verbose_name="Сообщение, которое пересылают")

    class Meta:
        unique_together = ('message', 'transfer',)
        indexes = [models.Index(fields=['message', 'transfer']),]
