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
    ADMIN_PERM = ((CREATOR, 'Создатель'),(CREATOR_ADMINS, 'Создатель и админы'),)

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
    can_edit_info = models.PositiveSmallIntegerField(choices=ALL_PERM, default=3, verbose_name="Кто редактирует информацию")
    can_fix_item = models.PositiveSmallIntegerField(choices=ALL_PERM, default=3, verbose_name="Кто закрепляет сообщения")
    can_mention = models.PositiveSmallIntegerField(choices=ALL_PERM, default=1, verbose_name="Кто упоминает о беседе")
    can_add_admin = models.PositiveSmallIntegerField(choices=ADMIN_PERM, default=3, verbose_name="Кто назначает админов")
    can_add_design = models.PositiveSmallIntegerField(choices=ALL_PERM, default=3, verbose_name="Кто меняет дизайн")

    class Meta:
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["order"]

    def __str__(self):
        return self.creator.get_full_name()

    def post_include_users(self, users, type):
        if type == "can_add_members":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_in_chat=1).update(can_add_in_chat=0)
        elif type == "can_edit_info":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_info=1).update(can_add_info=0)
        elif type == "can_fix_item":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_fix=1).update(can_add_fix=0)
        elif type == "can_add_admin":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_admin=1).update(can_add_admin=0)
        elif type == "can_mention":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_send_mention=1).update(can_send_mention=0)
        elif type == "can_add_design":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_design=1).update(can_add_design=0)
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
            elif type == "can_edit_info":
                perm.can_add_info = 1
                self.can_edit_info = 5
                self.save(update_fields=["can_edit_info"])
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
            perm.save()


    def post_exclude_users(self, users, type):
        if type == "can_add_members":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_in_chat=2).update(can_add_in_chat=0)
        elif type == "can_edit_info":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_info=2).update(can_add_info=0)
        elif type == "can_fix_item":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_fix=2).update(can_add_fix=0)
        elif type == "can_add_admin":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_admin=2).update(can_add_admin=0)
        elif type == "can_mention":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_send_mention=2).update(can_send_mention=0)
        elif type == "can_add_design":
            ChatPerm.objects.filter(user__chat_id=self.pk, can_add_design=2).update(can_add_design=0)
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
            elif type == "can_edit_info":
                perm.can_add_info = 2
                self.can_edit_info = 4
                self.save(update_fields=["can_edit_info"])
            elif type == "can_fix_item":
                perm.can_add_fix = 2
                self.can_add_fix = 4
                self.save(update_fields=["can_add_fix"])
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
            perm.save()

    def create_image(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.image = photo_input
        self.save(update_fields=['image'])
        new_img = get_thumbnailer(self.image)['avatar'].url.replace('media/', '')
        self.image = new_img
        return self.save(update_fields=['image'])

    def is_user_can_add_members(self, user):
        if self.can_add_members == self.ALL_CAN:
            return True
        elif self.can_add_members == self.CREATOR and self.creator.pk == user.pk:
            return True
        elif self.can_add_members == self.CREATOR_ADMINS and user.is_administrator_of_chat(self.pk):
            return True
        elif self.can_add_members == self.MEMBERS_BUT and self.get_special_perm_for_user(user.pk, 1, 0):
            return True
        elif self.can_add_members == self.SOME_MEMBERS and self.get_special_perm_for_user(user.pk, 1, 1):
            return True
        return False
    def is_user_can_edit_info(self, user):
        if self.can_edit_info == self.ALL_CAN:
            return True
        elif self.can_edit_info == self.CREATOR and self.creator.pk == user.pk:
            return True
        elif self.can_edit_info == self.CREATOR_ADMINS and user.is_administrator_of_chat(self.pk):
            return True
        elif self.can_edit_info == self.MEMBERS_BUT and self.get_special_perm_for_user(user.pk, 2, 0):
            return True
        elif self.can_edit_info == self.SOME_MEMBERS and self.get_special_perm_for_user(user.pk, 2, 1):
            return True
        return False
    def is_user_can_fix_item(self, user):
        if self.can_fix_item == self.ALL_CAN:
            return True
        elif self.can_fix_item == self.CREATOR and self.creator.pk == user.pk:
            return True
        elif self.can_fix_item == self.CREATOR_ADMINS and user.is_administrator_of_chat(self.pk):
            return True
        elif self.can_fix_item == self.MEMBERS_BUT and self.get_special_perm_for_user(user.pk, 3, 0):
            return True
        elif self.can_fix_item == self.SOME_MEMBERS and self.get_special_perm_for_user(user.pk, 3, 1):
            return True
        return False
    def is_user_can_mention(self, user):
        if self.can_mention == self.ALL_CAN:
            return True
        elif self.can_mention == self.CREATOR and self.creator.pk == user.pk:
            return True
        elif self.can_mention == self.CREATOR_ADMINS and user.is_administrator_of_chat(self.pk):
            return True
        elif self.can_mention == self.MEMBERS_BUT and self.get_special_perm_for_user(user.pk, 4, 0):
            return True
        elif self.can_mention == self.SOME_MEMBERS and self.get_special_perm_for_user(user.pk, 4, 1):
            return True
        return False
    def is_user_can_add_admin(self, user):
        if self.can_add_admin == self.ALL_CAN:
            return True
        elif self.can_add_admin == self.CREATOR and self.creator.pk == user.pk:
            return True
        elif self.can_add_admin == self.CREATOR_ADMINS and user.is_administrator_of_chat(self.pk):
            return True
        return False
    def is_user_can_add_design(self, user):
        if self.can_mention == self.ALL_CAN:
            return True
        elif self.can_add_design == self.CREATOR and self.creator.pk == user.pk:
            return True
        elif self.can_add_design == self.CREATOR_ADMINS and user.is_administrator_of_chat(self.pk):
            return True
        elif self.can_add_design == self.MEMBERS_BUT and self.get_special_perm_for_user(user.pk, 5, 0):
            return True
        elif self.can_add_design == self.SOME_MEMBERS and self.get_special_perm_for_user(user.pk, 5, 1):
            return True


    def get_special_perm_for_user(self, user_id, type, value):
        """
        type 1 - can_add_members, 2 - can_edit_info, 3 - can_fix_item, 4 - can_mention, 5 - can_add_design
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
                elif type == 2:
                    return ie.can_add_info != 2
                elif type == 3:
                    return ie.can_add_fix != 2
                elif type == 4:
                    return ie.can_send_mention != 2
                elif type == 5:
                    return ie.can_add_design != 2
            except ChatPerm.DoesNotExist:
                 return True
        elif value == 1:
            try:
                ie = member.chat_ie_settings
                if type == 1:
                    return ie.can_add_in_chat == 1
                elif type == 2:
                    return ie.can_add_info == 1
                elif type == 3:
                    return ie.can_add_fix == 1
                elif type == 4:
                    return ie.can_send_mention == 1
                elif type == 5:
                    return ie.can_add_design == 1
            except ChatPerm.DoesNotExist:
                 return False

    def is_private(self):
        return self.type == Chat.PRIVATE
    def is_group(self):
        return self.type == Chat.GROUP
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

    def get_recipients(self, exclude_creator_pk):
        from users.models import User
        return User.objects.filter(chat_users__chat__pk=self.pk, chat_users__type="ACT").exclude(pk=exclude_creator_pk)

    def get_recipients_2(self, exclude_creator_pk):
        return ChatUsers.objects.filter(chat_id=self.pk, type="ACT").exclude(user_id=exclude_creator_pk)

    def get_members_ids(self):
        users = self.get_members().values('id')
        return [_user['id'] for _user in users]

    def get_recipients_ids(self, exclude_creator_pk):
        users = self.get_recipients(exclude_creator_pk).values('id')
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
        query = Q(recipient_id=user_id)|Q(type=Message.MANAGER)
        query.add(~Q(type__contains="_"), Q.AND)
        return self.chat_message.filter(query).first()

    def get_messages(self):
        return self.chat_message.exclude(type__contains="_")

    def get_messages_uuids(self):
        messages = self.chat_message.exclude(type__contains="_").values('uuid')
        return [i['uuid'] for i in messages]

    def get_attach_photos(self):
        from gallery.models import Photo
        return Photo.objects.filter(message__uuid__in=self.get_messages_uuids())

    def get_unread_count_message(self, user_id):
        count = 0
        for message in Message.objects.filter(chat_id=self.pk,recipient_id=user_id, unread=True):
            if message.creator.pk != user_id:
                count += 1
        if count:
            return ''.join(['<span style="font-size: 80%;" class="tab_badge badge-success">', str(count), '</span>'])
        else:
            return ""

    def get_unread_message(self, user_id):
        return self.chat_message.filter(recipient_id=user_id, unread=True)

    def get_messages_for_recipient(self, user_id):
        query = Q(recipient_id=user_id)|Q(type=Message.MANAGER)
        query.add(~Q(type__contains="_"), Q.AND)
        return self.chat_message.filter(query)

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
            if message.get_type_text():
                preview_text = 'Черновик: ' + message.get_type_text()
            else:
                if first_message.creator.id == user_id:
                    preview_text = 'Вы: ' + first_message.get_type_text()
                else:
                    preview_text = first_message.get_type_text()
        elif not first_message:
            preview_text = "Нет сообщений"
        elif first_message.is_manager():
            if first_message.copy:
                creator = first_message.creator
                message = first_message.copy
                preview_text = creator.get_full_name() + first_message.text + '<span class="underline">' + message.get_text_60() + '</span>'
        else:
            preview_text = first_message.get_text_60()
            if first_message.creator.id == user_id:
                preview_text = 'Вы: ' + first_message.get_type_text()
            else:
                preview_text = first_message.get_type_text()
            if user_id == first_message.creator.pk and not first_message.is_copy_reed():
                is_read = ' bg-light-secondary'
            created = first_message.get_created()

        request_chat_user = self.get_chat_request_user(user_id)

        if self.is_private():
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
            media_body = ''.join(['<div class="media-body"><h5 class="time-title mb-0">', chat_name, request_chat_user.get_beep_icon(), status, '<small class="float-right text-muted">', created, '</small></h5><p class="mb-0', is_read ,'" style="white-space: nowrap;">', preview_text, '</p><span class="typed"></span></div>'])
            return ''.join(['<div class="media">', figure, media_body, self.get_unread_count_message(user_id), '</div>'])
        elif self.is_group():
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

    def get_avatars(self):
        urls = []
        for user in self.chat_relation.all()[:10]:
            i = user.user
            urls += '<a href="', i.get_link() ,'" target="_blank" tooltip="', i.get_full_name() ,'" flow="down">' + i.get_s_avatar() + '</a>'
        return urls

    def get_header_private_chat(self, user_id):
        buttons = '<span class="console_btn_other btn_default" style="display:none;"><span class="one_message"><span tooltip="Закрепить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_fixed" fill="currentColor" viewBox="0 0 24 24"><g><rect fill="none" height="24" width="24"/></g><g><path d="M16,9V4l1,0c0.55,0,1-0.45,1-1v0c0-0.55-0.45-1-1-1H7C6.45,2,6,2.45,6,3v0 c0,0.55,0.45,1,1,1l1,0v5c0,1.66-1.34,3-3,3h0v2h5.97v7l1,1l1-1v-7H19v-2h0C17.34,12,16,10.66,16,9z" fill-rule="evenodd"/></g></svg></span><span tooltip="Ответить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_reply" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z"/></svg></span><span tooltip="Пожаловаться" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_claim" viewBox="0 0 24 24" fill="currentColor"><path d="M11 15h2v2h-2v-2zm0-8h2v6h-2V7zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/></svg></span><span tooltip="Редактировать" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_edit" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg></span></span><span tooltip="Отметить как важное" flow="up"><svg class="toggle_message_favourite svg_default_30 mr-1 pointer" fill="currentColor" enable-background="new 0 0 24 24" viewBox="0 0 24 24"><g><rect x="0"></rect><polygon points="14.43,10 12,2 9.57,10 2,10 8.18,14.41 5.83,22 12,17.31 18.18,22 15.83,14.41 22,10"></polygon></g></svg></span><span tooltip="Удалить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_delete" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4h-3.5z"/></svg></span><span tooltip="Переслать" flow="up"><svg class="svg_default_30 pointer u_message_transfer" viewBox="0 0 24 24" fill="currentColor"><path d="m0 0h24v24h-24z" fill="none"/><path fill="currentColor" d="m12.1 7.87v-3.47a1.32 1.32 0 0 1 2.17-1l8.94 7.6a1.32 1.32 0 0 1 .15 1.86l-.15.15-8.94 7.6a1.32 1.32 0 0 1 -2.17-1v-3.45c-4.68.11-8 1.09-9.89 2.87a1.15 1.15 0 0 1 -1.9-1.11c1.53-6.36 5.51-9.76 11.79-10.05zm1.8-2.42v4.2h-.9c-5.3 0-8.72 2.25-10.39 6.86 2.45-1.45 5.92-2.16 10.39-2.16h.9v4.2l7.71-6.55z" /></svg></span></span>'
        chat_user = self.get_chat_user(user_id)
        request_chat_user = self.get_chat_request_user(user_id)
        member = chat_user.user
        #if self.image:
        #    figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:30px;width:30px;" alt="image"></figure>'])
        #elif member.s_avatar:
        #    figure = ''.join(['<figure><img src="', member.s_avatar.url,'" style="border-radius:30px;width:30px;" alt="image"></figure>'])
        #else:
        #    figure = '<figure><svg fill="currentColor" class="svg_default_30" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
        if self.name:
             chat_name = self.name
        else:
            chat_name = member.get_full_name()
        figure = ''
        media_body = ''.join(['<div class="media-body" style="overflow: inherit;"><h5 class="time-title mb-1"><a href="', member.get_link(), '" target="_blank">', chat_name, '<span class="notify_box">', request_chat_user.get_beep_icon(), '</span></a></h5><span class="mt-1 mb-2 target_display"><span class="type_display small" style="position:absolute;left:72px;top: 19px;">', member.get_online_status(), '</span>', buttons, '</span></div>'])
        return ''.join(['<a href="', member.get_link(), '" target="_blank">', figure, '</a>', media_body])

    def get_header_group_chat(self, user_id):
        chat_user = self.get_chat_user(user_id)
        request_chat_user = self.get_chat_request_user(user_id)
        buttons = '<span class="console_btn_other btn_default" style="display:none;padding-top:5px"><span class="one_message"><span tooltip="Закрепить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_fixed" fill="currentColor" viewBox="0 0 24 24"><g><rect fill="none" height="24" width="24"/></g><g><path d="M16,9V4l1,0c0.55,0,1-0.45,1-1v0c0-0.55-0.45-1-1-1H7C6.45,2,6,2.45,6,3v0 c0,0.55,0.45,1,1,1l1,0v5c0,1.66-1.34,3-3,3h0v2h5.97v7l1,1l1-1v-7H19v-2h0C17.34,12,16,10.66,16,9z" fill-rule="evenodd"/></g></svg></span><span tooltip="Ответить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_reply" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z"/></svg></span><span tooltip="Пожаловаться" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_claim" viewBox="0 0 24 24" fill="currentColor"><path d="M11 15h2v2h-2v-2zm0-8h2v6h-2V7zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/></svg></span><span tooltip="Редактировать" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_edit" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg></span></span><span tooltip="Отметить как важное" flow="up"><svg class="toggle_message_favourite svg_default_30 mr-1 pointer" fill="currentColor" enable-background="new 0 0 24 24" viewBox="0 0 24 24"><g><rect x="0"></rect><polygon points="14.43,10 12,2 9.57,10 2,10 8.18,14.41 5.83,22 12,17.31 18.18,22 15.83,14.41 22,10"></polygon></g></svg></span><span tooltip="Удалить" flow="up"><svg class="svg_default_30 mr-1 pointer u_message_delete" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4h-3.5z"/></svg></span><span tooltip="Переслать" flow="up"><svg class="svg_default_30 pointer u_message_transfer" viewBox="0 0 24 24" fill="currentColor"><path d="m0 0h24v24h-24z" fill="none"/><path fill="currentColor" d="m12.1 7.87v-3.47a1.32 1.32 0 0 1 2.17-1l8.94 7.6a1.32 1.32 0 0 1 .15 1.86l-.15.15-8.94 7.6a1.32 1.32 0 0 1 -2.17-1v-3.45c-4.68.11-8 1.09-9.89 2.87a1.15 1.15 0 0 1 -1.9-1.11c1.53-6.36 5.51-9.76 11.79-10.05zm1.8-2.42v4.2h-.9c-5.3 0-8.72 2.25-10.39 6.86 2.45-1.45 5.92-2.16 10.39-2.16h.9v4.2l7.71-6.55z" /></svg></span></span>'
        #if self.image:
        #    figure = ''.join(['<figure><img src="', self.image.url, '" style="border-radius:30px;width:30px;" alt="image"></figure>'])
        #else:
        #    figure = '<svg class="svg_default_30" style="margin-bottom:5px" fill="currentColor" viewBox="0 0 24 24"><rect fill="none" height="24" width="24"/><g><path d="M4,13c1.1,0,2-0.9,2-2c0-1.1-0.9-2-2-2s-2,0.9-2,2C2,12.1,2.9,13,4,13z M5.13,14.1C4.76,14.04,4.39,14,4,14 c-0.99,0-1.93,0.21-2.78,0.58C0.48,14.9,0,15.62,0,16.43V18l4.5,0v-1.61C4.5,15.56,4.73,14.78,5.13,14.1z M20,13c1.1,0,2-0.9,2-2 c0-1.1-0.9-2-2-2s-2,0.9-2,2C18,12.1,18.9,13,20,13z M24,16.43c0-0.81-0.48-1.53-1.22-1.85C21.93,14.21,20.99,14,20,14 c-0.39,0-0.76,0.04-1.13,0.1c0.4,0.68,0.63,1.46,0.63,2.29V18l4.5,0V16.43z M16.24,13.65c-1.17-0.52-2.61-0.9-4.24-0.9 c-1.63,0-3.07,0.39-4.24,0.9C6.68,14.13,6,15.21,6,16.39V18h12v-1.61C18,15.21,17.32,14.13,16.24,13.65z M8.07,16 c0.09-0.23,0.13-0.39,0.91-0.69c0.97-0.38,1.99-0.56,3.02-0.56s2.05,0.18,3.02,0.56c0.77,0.3,0.81,0.46,0.91,0.69H8.07z M12,8 c0.55,0,1,0.45,1,1s-0.45,1-1,1s-1-0.45-1-1S11.45,8,12,8 M12,6c-1.66,0-3,1.34-3,3c0,1.66,1.34,3,3,3s3-1.34,3-3 C15,7.34,13.66,6,12,6L12,6z"/></g></svg>'
        if self.name:
             chat_name = self.name
        else:
            chat_name = "Групповой чат"
        figure = ''
        media_body = ''.join(['<div class="media-body" style="overflow: inherit;"><h5 class="time-title mb-1"><span class="u_chat_info pointer">', chat_name, '</span><span class="notify_box">', request_chat_user.get_beep_icon(), '</h5><span class="mt-1 mb-2 target_display"><span class="u_chat_info pointer type_display small" style="position:absolute;left:25px;top: 19px;">', self.get_members_count_ru(), '</span>', buttons, '</span></div>'])
        return ''.join([media_body, figure])

    def is_not_empty(self):
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

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "pho" in self.attach:
            query = []
            from video.models import Video
            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)

    def get_draft_message(self, user_id):
        return Message.objects.filter(chat_id=self.pk, creator_id=user_id, type=Message.DRAFT).first()

    def is_have_draft_message(self, user_id):
        return Message.objects.filter(chat_id=self.pk, creator_id=user_id, type=Message.DRAFT).exists()

    def get_first_fix_message(self):
        if MessageFixed.objects.filter(chat_id=self.id).exists():
            return MessageFixed.objects.filter(chat_id=self.id).first()

    def get_fixed_messages(self):
        return MessageFixed.objects.filter(chat_id=self.id)

    def get_fix_message_count(self):
        if MessageFixed.objects.filter(chat_id=self.id).exists():
            return MessageFixed.objects.filter(chat_id=self.id).values("pk").count()
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
        if creator.is_women():
            var = "исключила"
        else:
            var = "исключил"
        ChatUsers.delete_member(user=user, chat=self)
        text = '<a target="_blank" href="' + creator.get_link() + '">' + creator.get_full_name() + '</a>&nbsp;' + var + '&nbsp;<a target="_blank" href="' + user.get_link() + '">' + user.get_full_name_genitive() + '</a>'
        info_message = Message.objects.create(chat_id=self.id,creator_id=creator.id,type=Message.MANAGER,text=text)
        for recipient in self.get_recipients_2(creator.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        return info_message

    def exit_member(self, user):
        if user.is_women():
            var = "вышла из чата"
        else:
            var = "вышел из чата"
        ChatUsers.exit_member(user=user, chat=self)
        text = '<a target="_blank" href="' + user.get_link() + '">' + user.get_full_name() + '</a>&nbsp;' + var
        info_message = Message.objects.create(chat_id=self.id,creator_id=user.id,type=Message.MANAGER,text=text)
        for recipient in self.get_recipients_2(user.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        return info_message

    def invite_users_in_chat(self, users_ids, creator):
        from users.models import User

        if creator.is_women():
            var = "пригласила"
        else:
            var = "пригласил"
        users = User.objects.filter(id__in=users_ids)
        info_messages = []
        for user in users:
            if (creator.is_administrator_of_chat(self.pk) and not ChatUsers.objects.filter(user=user, chat=self).exclude(type="DEL").exists()) \
            or not ChatUsers.objects.filter(user=user, chat=self).exists():
                member = ChatUsers.create_membership(user=user, chat=self)
                if member:
                    text = '<a target="_blank" href="' + creator.get_link() + '">' + creator.get_full_name() + '</a>&nbsp;' + var + '&nbsp;<a target="_blank" href="' + user.get_link() + '">' + user.get_full_name_genitive() + '</a>'
                    info_message = Message.objects.create(chat_id=self.id,creator_id=creator.id,type=Message.MANAGER,text=text)
                    info_messages.append(info_message)
                    for recipient in self.get_recipients_2(creator.pk):
                        info_message.create_socket(recipient.user.pk, recipient.beep())
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

    def get_can_edit_info_include_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_info=1).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in query])
    def get_can_edit_info_exclude_users(self):
        from users.models import User
        query = ChatUsers.objects.filter(chat_id=self.pk, chat_ie_settings__can_add_info=2).values("user_id")
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
        if not cls.objects.filter(user=user, chat=chat).exclude(type="DEL").exists():
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
            chat.members = chat.members - 1
            chat.save(update_fields=["members"])

    def delete_member(user, chat):
        # Человека удаляют из группового чата и он может вернуться только по приглашению админов
        if ChatUsers.objects.filter(user=user, chat=chat).exists():
            member = ChatUsers.objects.get(user=user, chat=chat)
            member.type = "DEL"
            member.save(update_fields=["type"])
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
    can_add_info = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто редактирует информацию")
    can_add_fix = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто закрепляет сообщения")
    can_send_mention = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто отправляет массовые упоминания")
    can_add_admin = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет админов и работает с ними")
    can_add_design = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто меняет дизайн")

    class Meta:
        verbose_name = 'Исключения/Включения участника беседы'
        verbose_name_plural = 'Исключения/Включения участников беседы'
        index_together = [('id', 'user'),]



class Message(models.Model):
    MANAGER, PUBLISHED, EDITED, DELETED, CLOSED, FIXED, FIXED_EDITED, DRAFT = 'MAN','PUB','EDI','_DEL','_CLO','_FIX','_FIXE','_DRA'
    DELETED_FIXED, DELETED_EDITED_FIXED, DELETED_EDITED, CLOSED_EDITED_FIXED, CLOSED_FIXED, CLOSED_EDITED = '_DELF','_DELFI','_DELE','_CLOFI','_CLOF','_CLOE'
    TYPE = (
        (MANAGER, 'Специальное'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(EDITED, 'Изменено'),(CLOSED, 'Закрыто модератором'),(DRAFT, 'Черновик'),
        (DELETED_FIXED, 'Удалённый закрепленный'),(DELETED_EDITED_FIXED, 'Удалённый измененный закрепленный'),(DELETED_EDITED, 'Удалённый измененный'),(CLOSED_EDITED, 'Закрытый измененный'),(CLOSED_EDITED_FIXED, 'Закрытый измененный закрепленный'),(CLOSED_FIXED, 'Закрытый закрепленный'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_creator', verbose_name="Создатель", null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_recipient', verbose_name="Получаетель", null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_message")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_thread")
    copy = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="message_copy")
    sticker = models.ForeignKey(Stickers, blank=True, null=True, on_delete=models.CASCADE, related_name="+")
    repost = models.ForeignKey("posts.Post", on_delete=models.CASCADE, null=True, blank=True, related_name='post_message')
    transfer = models.ManyToManyField("self", blank=True, related_name='+')

    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=5000, blank=True)
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

    def is_copy_reed(self):
        """ мы получаем копию сообщения любую. Если копия прочитана, значит возвращаем True
        Зачем это - при отрисовке первого сообщения правильно выводить кол-во непрочитанных. """
        for copy in self.message_copy.filter(copy=self).all():
            if not copy.unread:
                return True
        return False

    def get_draft_transfers_block(self):
        transfers = self.transfer.all()
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

    def is_have_transfer(self):
        if self.transfer.exists():
            return True

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

    def is_message_in_favourite(self, user_id):
        return MessageFavourite.objects.filter(message=self, user_id=user_id).exists()

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
        # получаем список чатов отправителя. Если получатель есть в одном из чатов, добавляем туда сообщение.
        # Если такого чата нет, создаем приватный чат, создаем по сообщению на каждого участника чата.

        chat_list, current_chat = creator.get_all_chats(), None
        _text = Message.get_format_text(text)
        for chat in chat_list:
            if user.pk in chat.get_members_ids() and chat.is_private():
                current_chat = chat
        if not current_chat:
            current_chat = Chat.objects.create(creator=creator, type=Chat.PRIVATE)
            ChatUsers.objects.create(user=creator, is_administrator=True, chat=current_chat)
            ChatUsers.objects.create(user=user, chat=current_chat)

        if voice:
            creator_message = Message.objects.create(chat=current_chat, creator=creator, recipient_id=creator.pk, repost=repost, voice=voice)
        elif sticker:
            creator_message = Message.objects.create(chat=current_chat, creator=creator, recipient_id=creator.pk, repost=repost, sticker_id=sticker)
            from common.model.other import UserPopulateStickers
            UserPopulateStickers.get_plus_or_create(user_pk=creator.pk, sticker_pk=sticker)
        else:
            creator_message = Message.objects.create(chat=current_chat, creator=creator, recipient_id=creator.pk, repost=repost, text=_text, attach=Message.get_format_attach(attach))
        for recipient in chat.get_recipients_2(creator.pk):
            if voice:
                recipient_message = Message.objects.create(chat=current_chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, voice=voice)
            elif sticker:
                recipient_message = Message.objects.create(chat=current_chat, copy=creator_message, sticker_id=sticker, recipient_id=recipient.user.pk, repost=repost, voice=voice)
            else:
                recipient_message = Message.objects.create(chat=current_chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, text=_text, attach=Message.get_format_attach(attach))
            recipient_message.create_socket(recipient.user.pk, recipient.beep())

    def create_chat_append_members_and_send_message(creator, users_ids, text, attach, voice, sticker):
        # Создаем коллективный чат и добавляем туда всех пользователей из полученного списка

        chat = Chat.objects.create(creator=creator, type=Chat.GROUP)
        _text = Message.get_format_text(text)

        if voice:
            creator_message = Message.objects.create(chat=chat, creator=creator, recipient_id=creator.pk, repost=repost, voice=voice)
        elif sticker:
            creator_message = Message.objects.create(chat=chat, creator=creator, recipient_id=creator.pk, repost=repost, sticker_id=sticker)
            from common.model.other import UserPopulateStickers
            UserPopulateStickers.get_plus_or_create(user_pk=creator.pk, sticker_pk=sticker)
        else:
            creator_message = Message.objects.create(chat=chat, creator=creator, recipient_id=creator.pk, repost=repost, text=_text, attach=Message.get_format_attach(attach))

        for recipient in chat.get_recipients_2(creator.pk):
            if voice:
                recipient_message = Message.objects.create(chat=chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, voice=voice)
            elif sticker:
                recipient_message = Message.objects.create(chat=chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, sticker_id=sticker)
            else:
                recipient_message = Message.objects.create(chat=chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, text=_text, attach=Message.get_format_attach(attach))
            recipient_message.create_socket(recipient.user.pk, recipient.beep())

    def send_message(chat, creator, repost, parent, text, attach, voice, sticker, transfer):
        # программа для отсылки сообщения в чате
        _text = Message.get_format_text(text)

        if parent:
            parent_id = parent
        else:
            parent_id = None
        if voice:
            creator_message = Message.objects.create(chat=chat, creator=creator, recipient_id=creator.pk, repost=repost, voice=voice, parent_id=parent_id)
        elif sticker:
            creator_message = Message.objects.create(chat=chat, creator=creator, recipient_id=creator.pk, repost=repost, sticker_id=sticker, parent_id=parent_id)
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
            creator_message = Message.objects.create(chat=chat, creator=creator, recipient_id=creator.pk, repost=repost, text=_text, attach=Message.get_format_attach(attach), parent_id=parent_id)
            if transfer:
                for i in transfer:
                    m = Message.objects.get(uuid=i)
                    creator_message.transfer.add(m)
            if chat.is_have_draft_message(creator.pk):
                message = chat.get_draft_message(creator.pk)
                message.text = ""
                message.attach = ""
                message.parent_id = None
                message.transfer.clear()
                message.save(update_fields=["text","attach","parent_id"])

        for recipient in chat.get_recipients_2(creator.pk):
            if voice:
                recipient_message = Message.objects.create(chat=chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, voice=voice, parent_id=parent_id)
            elif sticker:
                recipient_message = Message.objects.create(chat=chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, sticker_id=sticker, parent_id=parent_id)
            else:
                recipient_message = Message.objects.create(chat=chat, copy=creator_message, creator=creator, recipient_id=recipient.user.pk, repost=repost, text=_text, parent_id=parent_id, attach=Message.get_format_attach(attach))
            recipient_message.create_socket(recipient.user.pk, recipient.beep())
        return creator_message

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
            message = Message.objects.create(chat=chat, creator_id=creator.pk, recipient_id=creator.pk, text=text, attach=Message.get_format_attach(attach), parent_id=parent_id, type=Message.DRAFT)
        message.transfer.clear()
        if transfer:
            for i in transfer:
                m = Message.objects.get(uuid=i)
                message.transfer.add(m)

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'message',
            'chat_id': chat.pk,
            'recipient_ids': str(chat.get_recipients_ids(creator.pk)),
            'name': "u_message_typed",
            'user_name': creator.first_name,
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

    def fixed_message_for_user_chat(self, creator):
        """
            Мы должны пометить все сообшения ветки как FIXED.
            Для этого выясняем: это родительское сообщение, или имеет такое в поле copy.
            Его и все копированные помечаем и сохраняем. Создаем запись в таблице закрепленных сообщений,
            и в поле copy записываем сообшение, которое закрепляем. Мера нужна для показывания людям сообщения,
            которое открепили, чтобы новое поле не создавать, их и так много.
            Также создаем сокеты, чтобы участники чата увидели новое инфо-сообщение сразу
        """
        if self.copy:
            message = self.copy
            if message.type == "PUB":
                message.type = "_FIX"
            else:
                message.type = "_FIXE"
            message.save(update_fields=['type'])
            for i in Message.objects.filter(copy_id=message.pk):
                if i.type == "PUB":
                    i.type = "_FIX"
                else:
                    i.type = "_FIXE"
                i.save(update_fields=['type'])
        else:
            if self.type == "PUB":
                self.type = "_FIX"
            else:
                self.type = "_FIXE"
            self.save(update_fields=['type'])
            for i in Message.objects.filter(copy_id=self.pk):
                if i.type == "PUB":
                    i.type = "_FIX"
                else:
                    i.type = "_FIXE"
                i.save(update_fields=['type'])

        self.save(update_fields=['type'])
        fixed_message = MessageFixed.objects.create(chat_id=self.chat.id,creator_id=creator.id,message=self)
        if creator.is_women():
            var = " закрепила"
        else:
            var = " закрепил"
        text = var + " сообщение "
        info_message = Message.objects.create(chat_id=self.chat.id,creator_id=creator.id,type=Message.MANAGER,text=text,copy=self)
        for recipient in self.chat.get_recipients_2(creator.pk):
            info_message.create_socket(recipient.user.pk, recipient.beep())
        return info_message

    def unfixed_message_for_user_chat(self, creator):
        """
            Мы должны пометить все сообшения ветки как обычные или измененные.
            Для этого выясняем: это родительское сообщение, или имеет такое в поле copy.
            Его и все копированные помечаем и сохраняем. Создаем запись в таблице закрепленных сообщений,
            и в поле copy записываем сообшение, которое открепляем. Мера нужна для показывания людям сообщения,
            которое открепили, чтобы новое поле не создавать, их и так много.
            Также создаем сокеты, чтобы участники чата увидели новое инфо-сообщение сразу
        """
        if self.copy:
            message = self.copy
            if message.type == "_FIX":
                message.type = "PUB"
            else:
                message.type = "EDI"
            message.save(update_fields=['type'])
            for i in Message.objects.filter(copy_id=message.pk):
                if i.type == "_FIX":
                    i.type = "PUB"
                else:
                    i.type = "EDI"
                i.save(update_fields=['type'])
        else:
            if self.type == "_FIX":
                self.type = "PUB"
            else:
                self.type = "EDI"
            self.save(update_fields=['type'])
            for i in Message.objects.filter(copy_id=self.pk):
                if i.type == "_FIX":
                    i.type = "PUB"
                else:
                    i.type = "EDI"
                i.save(update_fields=['type'])

        if MessageFixed.objects.filter(chat_id=self.chat.id,message=self).exists():
            fixed_message = MessageFixed.objects.get(chat_id=self.chat.id,message=self).delete()
            if creator.is_women():
                var = " открепила"
            else:
                var = " открепил"
            text = var + " сообщение "
            info_message = Message.objects.create(chat_id=self.chat.id,creator_id=creator.id,type=Message.MANAGER,text=text,copy=self)
            for recipient in self.chat.get_recipients_2(creator.pk):
                info_message.create_socket(recipient.user.pk, recipient.beep())
            return info_message

    def edit_message(self, text, attach):
        from common.processing.message import get_edit_message_processing

        MessageVersion.objects.create(message=self, text=self.text, attach=self.attach.replace("<div class='attach_container'></div>", ""))
        if self.type == Message.PUBLISHED:
            self.type = Message.EDITED
        elif self.type == Message.FIXED:
            self.type = Message.FIXED_EDITED
        self.attach = self.get_attach(attach)
        self.text = text
        get_edit_message_processing(self)
        self.save()
        for copy in Message.objects.filter(copy_id=self.pk):
            copy.attach = self.attach
            copy.text = self.text
            copy.type = self.type
            copy.save()
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
            if self.transfer.all().count() > 1:
                return "<b class='i_link'>Пересланные сообщения</b>"
            else:
                return "<b class='i_link'>Пересланное сообщение</b>"
        elif self.parent:
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

    def get_preview_text(self):
        text = self.get_type_text()
        if self.is_manager():
            creator = self.creator
            message = self.copy
            return creator.get_full_name() + self.text + '<span class="underline">' + message.get_text_60() + '</span>'
        else:
            return text

    def get_manager_text(self):
        if self.copy:
            message = self.copy
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

    def delete_item(self, community):
        if self.type == "PUB":
            self.type = Message.DELETED
        elif self.type == "EDI":
            self.type = Message.DELETED_EDITED
        elif self.type == "_FIX":
            self.type = Message.DELETED_FIXED
        self.save(update_fields=['type'])
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Message.PUBLISHED
        elif self.type == "_DELE":
            self.type = Message.EDITED
        elif self.type == "_DELF":
            self.type = Message.FIXED
        self.save(update_fields=['type'])

    def close_item(self, community):
        if self.type == "PUB":
            self.type = Message.CLOSED
        elif self.type == "EDI":
            self.type = Message.CLOSED_EDITED
        elif self.type == "_FIX":
            self.type = Message.CLOSED_FIXED
        self.save(update_fields=['type'])
    def abort_close_item(self, community):
        if self.type == "_CLO":
            self.type = Message.PUBLISHED
        elif self.type == "_CLOE":
            self.type = Message.EDITED
        elif self.type == "_CLOF":
            self.type = Message.FIXED
        self.save(update_fields=['type'])


class MessageFavourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name="Добавивший", null=True, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='+', verbose_name="Сообщение", null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'message'),)
        verbose_name = 'Избранное сообщение'
        verbose_name_plural = 'Избранные сообщения'


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


class MessageFixed(models.Model):
    chat = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name="Чат", on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name="Тот, кто закрепил сообщение", null=True, on_delete=models.SET_NULL)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Закрепленное сообщение"
        verbose_name_plural = "Закрепленные сообщения"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.text

    def get_fixed_message_for_chat(self, chat_id, creator_id,):
        if self.type == "PUB":
            self.type = "_FIX"
        else:
            self.type = "_FIXE"
        self.save(update_fields=['type'])
        fixed_message = MessageFixed.objects.create(chat_id=chat_id,creator_id=creator_id,message=self)
        return fixed_message

    def get_unfixed_message_for_chat(self, chat_id):
        if self.type == "_FIX":
            self.type = "PUB"
        else:
            self.type = "EDI"
        self.save(update_fields=['type'])
        if MessageFixed.objects.filter(chat_id=chat_id,message=self).exists():
            fixed_message = MessageFixed.objects.get(chat_id=chat_id,message=self).delete()

    def get_preview_message(self):
        message = self.message
        if message.is_manager():
            creator = self.creator
            return '<i><a target="_blank" href="' + creator.get_link() + '">' + creator.get_full_name() + '</a>' + message.text + '</i>'
        elif message.is_have_transfer():
            if message.transfer.all().count() > 1:
                return "<b class='i_link'>Пересланные сообщения</b>"
            else:
                return "<b class='i_link'>Пересланное сообщение</b>"
        elif message.parent:
            return "<b class='i_link'>Ответ на сообщение</b>"
        elif message.attach:
            return "<b class='i_link'>Вложения</b>"
        elif message.voice:
            return "<b class='i_link'>Голосовое сообщение</b>"
        elif message.sticker:
            return "<b class='i_link'>Наклейка</b>"
        elif message.text:
            import re
            count = 60
            images = re.findall(r'<img.*?>', message.text)
            for image in images:
                count += (len(image) -1)
            return message.text[:count].replace("<br>", "  ")

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)
