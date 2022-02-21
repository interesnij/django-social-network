import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from common.utils import try_except
from common.check.user import *
from users.helpers import upload_to_user_directory


class User(AbstractUser):
    CHILD,PRIV_CHILD,STAND,PRIV_STAND,VER_SEND,PRIV_VER_SEND,VER,PRIV_VER,ID_SEND,PRIV_ID_SEND,ID,PRIV_ID= 'CHI','CHIP','STA','STAP','VES','VESP','VER','VERP','IDS','IDSP','IDE','IDEP'
    CLOS_CHILD,CLOS_PRIV_CHILD,CLOS_STAND,CLOS_PRIV_STAND,CLOS_VER_SEND,CLOS_PRIV_VER_SEND,CLOS_VER,CLOS_PRIV_VER,CLOS_ID_SEND,CLOS_PRIV_ID_SEND,CLOS_ID,CLOS_PRIV_ID = '_CLOC','_CLOCP','_CLOS','_CLOSP','_CLOVS','_CLOVSP','_CLOV','_CLOVP','_CLOIS','_CLOISP','_CLOI','_CLOIP'
    DEL_CHILD,DEL_PRIV_CHILD,DEL_STAND,DEL_PRIV_STAND,DEL_VER_SEND,DEL_PRIV_VER_SEND,DEL_VER,DEL_PRIV_VER,DEL_ID_SEND,DEL_PRIV_ID_SEND,DEL_ID,DEL_PRIV_ID = '_DELC','_DELCP', '_DELS','_DELSP', '_DELVS','_DELVSP', '_DELV','_DELVP', '_DELIS','_DELISP', '_DELI','_DELIP'
    SUSP_CHILD,SUSP_PRIV_CHILD,SUSP_STAND,SUSP_PRIV_STAND,SUSP_VER_SEND,SUSP_PRIV_VER_SEND, SUSP_VER,SUSP_PRIV_VER, SUSP_ID_SEND,SUSP_PRIV_ID_SEND,SUSP_ID,SUSP_PRIV_ID = '_SUSC','_SUSCP', '_SUSS','_SUSSP', '_SUSVS','_SUSVSP', '_SUSV','_SUSVP', '_SUSIS','_SUSISP', '_SUSI','_SUSIP'
    BAN_CHILD,BAN_PRIV_CHILD,BAN_STAND,BAN_PRIV_STAND,BAN_VER_SEND,BAN_PRIV_VER_SEND,BAN_VER,BAN_PRIV_VER,BAN_ID_SEND,BAN_PRIV_ID_SEND,BAN_ID,BAN_PRIV_ID = '_BANC','_BANCP', '_BANS','_BANSP', '_BANVS','_BANVSP', '_BANV','_BANVP', '_BANIS','_BANISP', '_BANI','_BANIP'

    STANDART,TRAINEE_MODERATOR, MODERATOR, HIGH_MODERATOR, TEAMLEAD_MODERATOR, \
    TRAINEE_MANAGER, MANAGER, \
    HIGH_MANAGER, TEAMLEAD_MANAGER,ADVERTISER, HIGH_ADVERTISER, TEAMLEAD_ADVERTISER,\
    ADMINISTRATOR, HIGH_ADMINISTRATOR, TEAMLEAD_ADMINISTRATOR,SUPERMANAGER = 1, 10,13,\
    16,19, 30,33,36,39, 40,44,49, 50,54,59, 60

    MALE, FEMALE, DESCTOP, PHONE = 'Man', 'Fem', 'De', 'Ph'

    TYPE = (
        (CHILD, 'Ребенок'),
        (PRIV_CHILD, 'Ребенок прив'),
        (STAND, 'Обычные права'),
        (PRIV_STAND, 'Обычный прив'),
        (VER_SEND, 'Запрос на проверку'),
        (PRIV_VER_SEND, 'Запрос на проверку прив'),
        (VER, 'Проверенный'),
        (PRIV_VER, 'Проверенный прив'),
        (ID_SEND, 'Запрос на ид'),
        (PRIV_ID_SEND, 'Запрос на ид прив'),
        (ID, 'Ид'),
        (PRIV_ID, 'Ид прив'),

        (DEL_CHILD, 'Удал ребенок'),
        (DEL_PRIV_CHILD, 'Удал ребенок прив'),
        (DEL_STAND, 'Удал'),
        (DEL_PRIV_STAND, 'Удал прив'),
        (DEL_VER_SEND, 'Удал подавший на вер'),
        (DEL_PRIV_VER_SEND, 'Удал подавший на вер прив'),
        (DEL_VER, 'Удал вер'),
        (DEL_PRIV_VER, 'Удал вер прив'),
        (DEL_ID_SEND, 'Удал подавший на ид'),
        (DEL_PRIV_ID_SEND, 'Удал подавший на ид прив'),
        (DEL_ID, 'Удал ид'),
        (DEL_PRIV_ID, 'Удал ид прив'),

        (CLOS_CHILD, 'Закр ребенок'),
        (CLOS_PRIV_CHILD, 'Закр ребенок прив'),
        (CLOS_STAND, 'Закр'),
        (CLOS_PRIV_STAND, 'Закр прив'),
        (CLOS_VER_SEND, 'Удал подавший на вер'),
        (CLOS_PRIV_VER_SEND, 'Удал подавший на вер прив'),
        (CLOS_VER, 'Закр вер'),
        (CLOS_PRIV_VER, 'Закр вер прив'),
        (CLOS_ID_SEND, 'Зак подавший на ид'),
        (CLOS_PRIV_ID_SEND, 'Закр подавший на ид прив'),
        (CLOS_ID, 'Закр ид'),
        (CLOS_PRIV_ID, 'Закр ид прив'),

        (SUSP_CHILD, 'Зам ребенок'),
        (SUSP_PRIV_CHILD, 'Зам ребенок прив'),
        (SUSP_STAND, 'Зам'),
        (SUSP_PRIV_STAND, 'Зам прив'),
        (SUSP_VER_SEND, 'Зам подавший на вер'),
        (SUSP_PRIV_VER_SEND, 'Зам подавший на вер прив'),
        (SUSP_VER, 'Зам вер'),
        (SUSP_PRIV_VER, 'Зам вер прив'),
        (SUSP_ID_SEND, 'Зам подавший на ид'),
        (SUSP_PRIV_ID_SEND, 'Зам подавший на ид прив'),
        (SUSP_ID, 'Зам ид'),
        (SUSP_PRIV_ID, 'Зам ид прив'),

        (BAN_CHILD, 'Бан ребенок'),
        (BAN_PRIV_CHILD, 'Бан ребенок прив'),
        (BAN_STAND, 'Бан'),
        (BAN_PRIV_STAND, 'Бан прив'),
        (BAN_VER_SEND, 'Бан подавший на вер'),
        (BAN_PRIV_VER_SEND, 'Бан подавший на вер прив'),
        (BAN_VER, 'Бан вер'),
        (BAN_PRIV_VER, 'Бан вер прив'),
        (BAN_ID_SEND, 'Бан подавший на ид'),
        (BAN_PRIV_ID_SEND, 'Бан подавший на ид прив'),
        (BAN_ID, 'Бан ид'),
        (BAN_PRIV_ID, 'Бан ид прив'),
    )
    PERM = (
        (STANDART, 'Обычные права'),
        (TRAINEE_MODERATOR,'Модератор-стажер'),(MODERATOR,'Модератор'),(HIGH_MODERATOR,'Старший модератор'),(TEAMLEAD_MODERATOR, 'Модератор-тимлид'),
        (TRAINEE_MANAGER, 'Менеджер-стажер'),(MANAGER, 'Менеджер'),(HIGH_MANAGER,'Старший менеджер'),(TEAMLEAD_MANAGER, 'Менеджер-тимлид'),
        (ADVERTISER, 'Менеджер рекламы'),(HIGH_ADVERTISER,'Старший менеджер рекламы'),(TEAMLEAD_ADVERTISER, 'Менеджер-тимлид рекламы'),
        (ADMINISTRATOR, 'Администратор'),(HIGH_ADMINISTRATOR,'Старший администратор'),(TEAMLEAD_ADMINISTRATOR, 'Администратор-тимлид'),
        (SUPERMANAGER, 'Суперменеджер'),
    )
    GENDER = ((MALE, 'Мужской'),(FEMALE, 'Женский'),)
    DEVICE = ((DESCTOP, 'Комп'),(PHONE, 'Телефон'),)

    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, unique=True, verbose_name='Телефон')
    type = models.CharField(max_length=8, choices=TYPE, default=STANDART, verbose_name="Уровень доступа")
    gender = models.CharField(max_length=5, choices=GENDER, blank=True, verbose_name="Пол")
    device = models.CharField(max_length=5, choices=DEVICE, blank=True, verbose_name="Оборудование")
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    have_link = models.CharField(max_length=17, blank=True, verbose_name='Ссылка')
    sity = models.CharField(max_length=settings.PROFILE_LOCATION_MAX_LENGTH, blank=True, verbose_name="Местоположение")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    language = models.CharField(max_length=7, choices=settings.LANGUAGES, default="ru")
    perm = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Статус пользователя")
    level = models.PositiveSmallIntegerField(default=100, verbose_name="Порядочность")
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()

    def close_item(self):
        if self.type == "STA":
            self.type = User.CLOSED_STANDART
        elif self.type == "DEPS":
            self.type = User.CLOSED_DEPUTAT_SEND
        elif self.type == "STA":
            self.type = User.CLOSED_STANDART
        elif self.type == "MAN":
            self.type = User.CLOSED_MANAGER
        elif self.type == "IDS":
            self.type = User.CLOSED_IDENTIFIED_SEND
        elif self.type == "IDE":
            self.type = User.CLOSED_IDENTIFIED
        self.save(update_fields=['type'])
    def abort_close_item(self):
        if self.type == "_CLOD":
            self.type = User.DEPUTAT
        elif self.type == "_CLODS":
            self.type = User.DEPUTAT_SEND
        elif self.type == "_CLOS":
            self.type = User.STANDART
        elif self.type == "_CLOM":
            self.type = User.MANAGER
        elif self.type == "_CLOIS":
            self.type = User.IDENTIFIED_SEND
        elif self.type == "_CLOI":
            self.type = User.IDENTIFIED
        self.save(update_fields=['type'])

    def suspend_item(self):
        if self.type == "DEP":
            self.type = User.SUSPENDED_DEPUTAT
        elif self.type == "DEPS":
            self.type = User.SUSPENDED_DEPUTAT_SEND
        elif self.type == "STA":
            self.type = User.SUSPENDED_STANDART
        elif self.type == "MAN":
            self.type = User.SUSPENDED_MANAGER
        elif self.type == "IDS":
            self.type = User.SUSPENDED_IDENTIFIED_SEND
        elif self.type == "IDE":
            self.type = User.SUSPENDED_IDENTIFIED
        self.save(update_fields=['type'])
    def abort_suspend_item(self):
        if self.type == "_SUSD":
            self.type = User.DEPUTAT
        elif self.type == "_SUSDS":
            self.type = User.DEPUTAT
        elif self.type == "_SUSS":
            self.type = User.STANDART
        elif self.type == "_SUSM":
            self.type = User.MANAGER
        elif self.type == "_SUSIS":
            self.type = User.IDENTIFIED_SEND
        elif self.type == "_SUSI":
            self.type = User.IDENTIFIED
        self.save(update_fields=['type'])

    def get_description(self):
        return '<a href="' + self.get_link() + '" target="_blank">' + self.get_full_name_genitive() + '</a>'

    def is_can_work_list(self, list):
        return (list.community and self.pk in list.community.get_administrators_ids()) \
        or self.pk == list.creator.pk

    def get_code(self):
        return "use" + str(self.pk)
    def is_user(self):
        return True

    def get_or_create_manager_chat_pk(self):
        from chat.models import Chat, ChatUsers
        if Chat.objects.filter(creator_id=self.pk, type=Chat.MANAGER).exists():
            return Chat.objects.filter(creator_id=self.pk, type=Chat.MANAGER).first().pk
        else:
            chat = Chat.objects.create(creator_id=self.pk, type=Chat.MANAGER, name="Рассылка служународу.рус",)
            ChatUsers.objects.create(user=self, chat=chat)
            return chat.pk
    def get_or_create_support_chat_pk(self):
        from chat.models import Chat, ChatUsers
        if Chat.objects.filter(creator_id=self.pk, type__contains="SUP").exists():
            return Chat.objects.filter(creator_id=self.pk, type__contains="SUP").first().pk
        else:
            chat = Chat.objects.create(creator_id=self.pk, type=Chat.SUPPORT_1, name="Чат техподдержки",)
            ChatUsers.objects.create(user=self, chat=chat)
            return chat.pk
    def is_have_deleted_support_chats(self):
        from chat.models import Chat, ChatUsers
        return Chat.objects.filter(creator_id=self.pk, type__contains="_SUP").exists()
    def get_deleted_support_chats(self):
        from chat.models import Chat, ChatUsers
        return Chat.objects.filter(creator_id=self.pk, type__contains="_SUP")

    def is_closed_profile(self):
        return self.type[-1] == "P"

    def get_last_location(self):
        from users.model.profile import UserLocation
        return UserLocation.objects.filter(user=self)[0]

    def get_favourite_messages(self):
        from chat.models import MessageOptions
        query = []
        for i in MessageOptions.objects.filter(user_id=self.pk, is_favourite=True):
            query.append(i.message)
        return query

    def favourite_messages_count(self):
        from chat.models import MessageOptions
        return MessageOptions.objects.filter(user_id=self.pk, is_favourite=True).values("pk").count()

    def get_fixed_posts(self):
        from posts.models import Post
        return Post.objects.filter(creator_id=self.pk, type="FIX")

    def get_fixed_posts_ids(self):
        from posts.models import Post
        list = Post.objects.filter(creator_id=self.pk, type="FIX").values("pk")
        return [i['pk'] for i in list]
    def count_fix_items(self):
        from posts.models import Post
        return Post.objects.filter(creator_id=self.pk, type="FIX").values("pk").count()

    def is_can_fixed_post(self):
        return self.count_fix_items() < 10

    def get_verb_gender(self, verb):
        if self.is_women():
            return "W" + verb
        else:
            return verb

    def get_populate_smiles(self):
        from common.model.other import Smiles, UserPopulateSmiles
        query = []
        for smile in UserPopulateSmiles.objects.filter(user_id=self.pk)[:20]:
            query.append(Smiles.objects.get(id=smile.pk))
        return query
    def is_have_populate_smiles(self):
        from common.model.other import Smiles
        return Smiles.objects.filter(smile__user_id=self.pk).exists()

    def get_populate_stickers(self):
        from common.model.other import UserPopulateStickers, Stickers
        stickers = UserPopulateStickers.objects.filter(user_id=self.pk)[:20]
        stickers_values = stickers.values("sticker_id")
        stickers_ids = [i['sticker_id'] for i in stickers_values]
        return Stickers.objects.filter(id__in=stickers_ids)
    def is_have_populate_stickers(self):
        from common.model.other import UserPopulateStickers
        return UserPopulateStickers.objects.filter(user_id=self.pk).exists()

    def get_device(self):
        if self.device == User.DESCTOP:
            return "De"
        else:
            return "Ph"

    def get_link(self):
        if self.have_link:
            return "/" + self.have_link + "/"
        else:
            return "/id" + str(self.pk) + "/"

    def get_slug(self):
        if self.have_link:
            return "@" + self.have_link
        else:
            return "@id" + str(self.pk)

    def get_color_background(self):
        try:
            return self.color_settings.color
        except:
            return "white"

    def get_last_activity(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.last_activity)

    def get_email_status(self):
        if self.email:
            return self.email
        else:
            return 'Почта не указана'

    def calculate_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def is_women(self):
        return self.gender == User.FEMALE
    def is_men(self):
        return self.gender == User.MALE

    def is_supermanager(self):
        return self.perm == 60 or self.is_superuser
    def is_administrator(self):
        return self.perm > 49 or self.is_superuser
    def is_advertiser(self):
        return self.perm > 39 or self.is_superuser
    def is_manager(self):
        return self.perm > 29 or self.is_superuser
    def is_support(self):
        return self.perm > 19 or self.is_superuser
    def is_moderator(self):
        return self.perm > 9 or self.is_superuser

    def is_suspended(self):
        return self.type[:4] == "_SUS"
    def is_have_warning_banner(self):
        return self.type[:4] == "_BAN"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_verified_send(self):
        return self.type == User.VER_SEND
    def is_verified(self):
        return self.type == User.VER
    def is_identified_send(self):
        return self.type == User.ID_SEND
    def is_identified(self):
        return self.type == User.ID
    def is_child(self):
        return self.type == User.CHILD
    def is_child_safety(self):
        if self.perm > 5  or self.type == User.VER:
            return True
        else:
            return False

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def get_full_name_genitive(self):
        import pymorphy2
        from string import ascii_letters

        morph = pymorphy2.MorphAnalyzer()
        if all(map(lambda c: c in ascii_letters, self.first_name)):
            first_name = self.first_name
        else:
            name = morph.parse(self.first_name)[0]
            v1 = name.inflect({'gent'})
            first_name = v1.word.title()
        if all(map(lambda c: c in ascii_letters, self.last_name)):
            last_name = self.last_name
        else:
            surname = morph.parse(self.last_name)[0]
            v2 = surname.inflect({'gent'})
            last_name = v2.word.title()
        return first_name + " " + last_name

    def get_name_genitive(self):
        import pymorphy2
        from string import ascii_letters

        morph = pymorphy2.MorphAnalyzer()
        if all(map(lambda c: c in ascii_letters, self.first_name)):
            first_name = self.first_name
        else:
            name = morph.parse(self.first_name)[0]
            v1 = name.inflect({'gent'})
            first_name = v1.word.title()
        return first_name

    def get_full_name_datv(self):
        import pymorphy2
        from string import ascii_letters

        morph = pymorphy2.MorphAnalyzer()
        if all(map(lambda c: c in ascii_letters, self.first_name)):
            first_name = self.first_name
        else:
            name = morph.parse(self.first_name)[0]
            v1 = name.inflect({'datv'})
            first_name = v1.word.title()
        if all(map(lambda c: c in ascii_letters, self.last_name)):
            last_name = self.last_name
        else:
            surname = morph.parse(self.last_name)[0]
            v2 = surname.inflect({'datv'})
            last_name = v2.word.title()
        return first_name + " " + last_name

    def create_s_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer
        self.s_avatar = photo_input
        self.save(update_fields=['s_avatar'])
        new_img = get_thumbnailer(self.s_avatar)['small_avatar'].url.replace('media/', '')
        self.s_avatar = new_img
        return self.save(update_fields=['s_avatar'])
    def create_b_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer
        self.b_avatar = photo_input
        self.save(update_fields=['b_avatar'])
        new_img = get_thumbnailer(self.b_avatar)['avatar'].url.replace('media/', '')
        self.b_avatar = new_img
        return self.save(update_fields=['b_avatar'])

    def get_b_avatar(self):
        if self.get_avatar_pk():
            return '<img src="' + self.b_avatar.url + '" class="detail_photo pointer" photo-pk="' + str(self.get_avatar_pk()) + '">'
        else:
            return '<img src="/static/images/no_img/b_avatar.png" />'

    def get_avatar(self):
        try:
            return self.s_avatar.url
        except:
            return "/static/images/no_img/list.jpg"
    def get_bb_avatar(self):
        try:
            return self.b_avatar.url
        except:
            return "/static/images/no_img/list.jpg"

    def get_s_avatar(self):
        if self.s_avatar:
            return '<img style="border-radius:30px;width:30px;" alt="image" src="' + self.s_avatar.url + '" />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_30" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
    def get_40_avatar(self):
        if self.s_avatar:
            return '<img style="border-radius:40px;width:40px;" alt="image" src="' + self.s_avatar.url + '" alt="image" />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_40" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'

    def get_my_avatar(self):
        if self.s_avatar:
            return '<img style="border-radius:50px;width:50px;" alt="image" src="' + self.s_avatar.url + '" />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'

    def get_online(self):
        from datetime import datetime, timedelta
        return datetime.now() < self.last_activity + timedelta(minutes=3)

    def get_online_display(self):
        from datetime import datetime, timedelta

        if self.device == User.DESCTOP:
            device = '&nbsp;<svg style="width: 17px;" class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 18c1.1 0 1.99-.9 1.99-2L22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zM4 6h16v10H4V6z"/></svg>'
        else:
            device = '&nbsp;<svg style="width: 17px;" class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>'
        if datetime.now() < self.last_activity + timedelta(minutes=3):
            return '<i>Онлайн</i>' + device
        else:
            if self.is_women():
                return '<i>Была ' + self.get_last_activity() + '</i>' + device
            else:
                return '<i>Был ' + self.get_last_activity() + '</i>' + device

    def get_online_status(self):
        from datetime import datetime, timedelta
        if datetime.now() < self.last_activity + timedelta(minutes=3):
            return '<i>Онлайн</i>'
        else:
            if self.is_women():
                return '<i>Была ' + self.get_last_activity() + '</i>'
            else:
                return '<i>Был ' + self.get_last_activity() + '</i>'

    def get_blocked_users(self):
        return User.objects.filter(blocked_by_users__blocker_id=self.pk).distinct()

    def get_staffed_communities(self):
        from communities.models import Community

        query = Q(Q(memberships__user=self, memberships__is_administrator=True) | Q(memberships__user=self, memberships__is_editor=True))
        return Community.objects.filter(query)

        '''''проги для подписчиков  60-109'''''

    def follow_user(self, user):
        from follows.models import Follow

        check_can_follow_user(user=self, user_id=user.pk)
        if self.pk == user.pk:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        follow = Follow.create_follow(user_id=self.pk, followed_user_id=user.pk)

        user.plus_follows(1)
        if not user.is_closed_profile():
            self.add_news_subscriber_in_main_list(user.pk)
            self.get_or_create_featured_objects_in_main_list(user)

    def community_follow_user(self, community_pk):
        return self.follow_community(community_pk)

    def follow_community(self, community):
        from follows.models import CommunityFollow

        check_can_join_community(user=self, community_pk=community.pk)
        community.create_community_notify(self.pk)
        return CommunityFollow.create_follow(user_id=self.pk, community_pk=community_pk)

    def community_unfollow_user(self, community):
        return self.unfollow_community(community)

    def unfollow_community(self, community):
        from follows.models import CommunityFollow

        check_can_join_community(user=self, community_pk=community.pk)
        follow = CommunityFollow.objects.get(user=self,community__pk=community.pk)
        follow.delete()
        community.delete_community_notify(self.pk)

    def plus_friend_visited(self, user_id):
        from frends.models import Connect
        frend = Connect.objects.get(user_id=self.pk, target_user_id=user_id)
        frend.visited = frend.visited + 1
        frend.save(update_fields=["visited"])

    def plus_community_visited(self, community_id):
        from communities.models import CommunityMembership
        if CommunityMembership.objects.filter(community_id=community_id, user_id=self.pk).exists():
            member = CommunityMembership.objects.filter(community_id=community_id, user_id=self.pk).first()
            member.visited = member.visited + 1
            member.save(update_fields=["visited"])

    def remove_featured_friend_from_all_list(self, user_id):
        from users.model.list import ListUC, FeaturedUC
        if FeaturedUC.objects.filter(owner=self.pk, user=user_id).exists():
            FeaturedUC.objects.filter(owner=self.pk, user=user_id).delete()
    def remove_featured_friend_from_list(self, user_id, list_id):
        from users.model.list import ListUC, FeaturedUC
        if FeaturedUC.objects.filter(list_id=list_id, owner=self.pk, user=user_id).exists():
            FeaturedUC.objects.filter(list_id=list_id, owner=self.pk, user=user_id).delete()

    def remove_featured_communities_from_all_list(self, community_id):
        from users.model.list import ListUC, FeaturedUC
        if FeaturedUC.objects.filter(owner=self.pk, community=community_id).exists():
            FeaturedUC.objects.filter(owner=self.pk, community=community_id).delete()
    def remove_featured_communities_from_list(self, community_id, list_id):
        from users.model.list import ListUC, FeaturedUC
        if FeaturedUC.objects.filter(list_id=list_id, owner=self.pk, community=community_id).exists():
            FeaturedUC.objects.filter(list_id=list_id, owner=self.pk, community=community_id).delete()

    def frend_user(self, user):
        self.get_or_create_featured_objects_in_main_list(user)
        self.frend_user_with_id(user.pk)
        user.plus_friends(1)
        self.plus_friends(1)
        self.minus_follows(1)
        if user.is_closed_profile():
            self.add_news_subscriber_in_main_list(user.pk)

    def frend_user_with_id(self, user_id):
        from follows.models import Follow
        from frends.models import Connect

        check_can_connect_with_user(user=self, user_id=user_id)
        if self.pk == user_id:
            raise ValidationError('Вы не можете добавить сами на себя',)
        frend = Connect.create_connection(user_id=self.pk, target_user_id=user_id)
        follow = Follow.objects.get(user=user_id, followed_user_id=self.pk)
        follow.delete()
        self.remove_featured_friend_from_all_list(user_id)
        return frend

    def get_featured_friends_ids(self):
        from users.model.list import ListUC, FeaturedUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        return [i['user'] for i in FeaturedUC.objects.filter(list=list, owner=self.pk, mute=False, community=0).values("user")]
    def get_6_featured_friends_ids(self):
        return self.get_featured_friends_ids()[:6]
    def get_featured_friends(self):
        return User.objects.filter(id__in=self.get_featured_friends_ids())
    def get_6_featured_friends(self):
        return User.objects.filter(id__in=self.get_6_featured_friends_ids())
    def get_featured_friends_count(self):
        return len(self.get_featured_friends_ids())

    def get_featured_communities_ids(self):
        from users.model.list import ListUC, FeaturedUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        return [i['community'] for i in FeaturedUC.objects.filter(list=list, owner=self.pk, mute=False, user=0).values("community")]
    def get_6_featured_communities_ids(self):
        return self.get_featured_communities_ids()[:6]
    def get_featured_communities(self):
        from communities.models import Community
        return Community.objects.filter(id__in=self.get_featured_communities_ids())
    def get_6_featured_communities(self):
        from communities.models import Community
        return Community.objects.filter(id__in=self.get_6_featured_communities_ids())
    def get_featured_communities_count(self):
        return len(self.get_featured_communities_ids())

    def unfollow_user(self, user):
        self.unfollow_user_with_id(user.pk)
        return user.minus_follows(1)

    def unfollow_user_with_id(self, user_id):
        from follows.models import Follow

        check_not_can_follow_user(user=self, user_id=user_id)
        follow = Follow.objects.get(user=self,followed_user_id=user_id).delete()
        self.delete_news_subscriber_from_main_list(user_id)

    def unfrend_user(self, user):
        self.unfrend_user_with_id(user.pk)
        user.minus_friends(1)
        self.minus_friends(1)
        self.plus_follows(1)
        return self

    def unfrend_user_with_id(self, user_id):
        from follows.models import Follow

        check_is_following_user(user=self, user_id=user_id)
        follow = Follow.create_follow(user_id=user_id, followed_user_id=self.pk)
        follow.view = True
        follow.save(update_fields=["view"])
        if self.is_closed_profile():
            self.delete_news_subscriber_from_main_list(user_id)
        connection = self.connections.get(target_connection__user_id=user_id)
        return connection.delete()

    def get_or_create_featured_objects_in_main_list(self, user):
        from users.model.list import ListUC, FeaturedUC

        try:
            list = ListUC.objects.get(type=1, owner=self.pk)
        except:
            list = ListUC.objects.create(type=1, name="Основной", owner=self.pk)

        for frend in user.get_6_friends():
            if frend.pk != self.pk and not FeaturedUC.objects.filter(owner=self.pk, user=frend.pk).exists():
                FeaturedUC.objects.create(list=list, owner=self.pk, user=frend.pk)
        for community in user.get_6_communities():
            if not FeaturedUC.objects.filter(owner=self.pk, community=community.pk).exists():
                FeaturedUC.objects.create(list=list, owner=self.pk, community=community.pk)

    def disconnect_from_user_with_id(self, user_id):
        check_is_connected(user=self, user_id=user_id)
        if self.is_following_user_with_id(user_id):
            self.unfollow_user_with_id(user_id)
        connection = self.connections.get(target_connection__user_id=user_id)
        connection.delete()

    def unblock_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        return self.unblock_user_with_id(user_id=user.pk)

    def unblock_user_with_id(self, user_id):
        check_can_unblock_user(user=self, user_id=user_id)
        self.user_blocks.filter(blocked_user_id=user_id).delete()
        return User.objects.get(pk=user_id)

    def block_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        return self.block_user_with_id(user_id=user.pk)

    def block_user_with_id(self, user_id):
        from users.model.list import UserBlock
        check_can_block_user(user=self, user_id=user_id)

        if self.is_connected_with_user_with_id(user_id=user_id):
            self.disconnect_from_user_with_id(user_id=user_id)
        if self.is_following_user_with_id(user_id=user_id):
            self.unfollow_user_with_id(user_id=user_id)

        user_to_block = User.objects.get(pk=user_id)
        if user_to_block.is_following_user_with_id(user_id=self.pk):
            user_to_block.unfollow_user_with_id(self.pk)

        UserBlock.create_user_block(blocker_id=self.pk, blocked_user_id=user_id)
        self.remove_featured_friend_from_all_list(user_id)
        self.delete_news_subscriber_from_main_list(user_id)
        self.delete_notify_subscriber_from_main_list(user_id)
        return user_to_block

    '''''проверки is для подписчиков  113-169'''''

    def is_connected_with_user(self, user):
        return self.is_connected_with_user_with_id(user.pk)

    def is_blocked_with_user_with_id(self, user_id):
        from users.model.list import UserBlock
        return UserBlock.users_are_blocked(user_a_id=self.pk, user_b_id=user_id)

    def is_connected_with_user_with_id(self, user_id):
        return self.connections.filter(target_connection__user_id=user_id).exists()

    def is_invited_to_community(self, community_pk):
        from communities.models import Community
        return Community.is_user_with_username_invited_to_community(username=self.username, community_pk=community_pk)

    def is_staff_of_community(self, community_pk):
        return self.is_administrator_of_community(community_pk=community_pk) or self.is_moderator_of_community(community_pk=community_pk) or self.is_editor_of_community(community_pk=community_pk)

    def is_member_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk).exists()

    def is_voted_of_survey(self, survey_pk):
        return self.user_voter.filter(answer__survey__pk=survey_pk).exists()
    def get_vote_of_survey(self, survey_pk):
        return self.user_voter.filter(answer__survey__pk=survey_pk)[0]

    def is_banned_from_community(self, community_pk):
        return self.banned_of_communities.filter(pk=community_pk).exists()

    def is_follow_from_community(self, community_pk):
        return self.community_follows.filter(community__pk=community_pk).exists()

    def is_creator_of_community(self, community_pk):
        return self.created_communities.filter(pk=community_pk).exists()

    def is_staffed_user(self):
        return self.communities_memberships.filter(Q(is_administrator=True) | Q(is_moderator=True) | Q(is_editor=True)).exists()
    def is_administrator_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_administrator=True).exists()
    def is_moderator_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_moderator=True).exists()
    def is_advertiser_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_advertiser=True).exists()
    def is_editor_of_community(self, community_pk):
        return self.communities_memberships.filter(community__pk=community_pk, is_editor=True).exists()

    def is_following_user_with_id(self, user_id):
        return self.follows.filter(followed_user__id=user_id).exists()
    def is_followers_user_with_id(self, user_id):
        return self.followers.filter(user__id=user_id).exists()
    def is_followers_user_view(self, user_id):
        return self.followers.filter(user__id=user_id, view=True).exists()

    def has_blocked_user_with_id(self, user_id):
        return self.user_blocks.filter(blocked_user_id=user_id).exists()

    def is_blocked_user_with_id(self, user_id):
        return self.blocked_by_users.filter(blocked_user_id=user_id).exists()

    def get_buttons_profile(self, user_id):
        if self.is_authenticated:
            if self.has_blocked_user_with_id(user_id):
                return "desctop/users/button/blocked_user.html"
            elif self.is_connected_with_user_with_id(user_id):
                return "desctop/users/button/frend_user.html"
            elif self.is_followers_user_view(user_id):
                return "desctop/users/button/follow_user.html"
            elif self.is_following_user_with_id(user_id):
                return "desctop/users/button/following_user.html"
            elif self.is_followers_user_with_id(user_id):
                return "desctop/users/button/follow_view_user.html"
            else:
                return "desctop/users/button/default_user.html"
        else:
            return "desctop/users/button/null_value.html"
    def get_staff_buttons_profile(self, user_id):
        if self.is_authenticated:
            if self.has_blocked_user_with_id(user_id):
                return "desctop/users/button/staff_blocked_user.html"
            elif self.is_connected_with_user_with_id(user_id):
                return "desctop/users/button/staff_frend_user.html"
            elif self.is_followers_user_view(user_id):
                return "desctop/users/button/staff_follow_user.html"
            elif self.is_following_user_with_id(user_id):
                return "desctop/users/button/staff_following_user.html"
            elif self.is_followers_user_with_id(user_id):
                return "desctop/users/button/staff_follow_view_user.html"
            else:
                return "desctop/users/button/staff_default_user.html"
        else:
            return "desctop/users/button/null_value.html"

    def is_photo_exists(self):
        return self.profile.photos > 0

    def is_track_exists(self, track_id):
        return self.profile.tracks > 0

    def is_user_playlist(self):
        from music.models import UserTempMusicList
        return UserTempMusicList.objects.filter(user=self, tag=None, genre=None).exists()

    def is_user_temp_list(self, list):
        from music.models import UserTempMusicList
        return UserTempMusicList.objects.filter(user=self, genre=None, list=list).exists()

    def is_genre_playlist(self, genre):
        from music.models import UserTempMusicList
        return UserTempMusicList.objects.get(user=self, tag=None, list=None, genre=genre).exists()

    ''''' количества всякие  196-216 '''''

    def is_no_view_followers(self):
        return self.followers.filter(view=False).exists()

    def is_have_followers(self):
        return self.profile.follows > 0
    def is_have_followings(self):
        return self.follows.values('pk').exists()
    def is_have_blacklist(self):
        return self.user_blocks.values('pk').exists()
    def is_have_friends(self):
        return self.profile.friends > 0
    def is_have_communities(self):
        return self.profile.communities > 0
    def is_have_music(self):
        return self.profile.tracks > 0
    def is_have_photo(self):
        return self.profile.photos > 0
    def is_have_video(self):
        return self.profile.videos > 0
    def is_have_doc(self):
        return self.profile.docs > 0
    def is_have_post(self):
        return self.profile.posts > 0

    def count_no_view_followers(self):
        return self.followers.filter(view=False).values('pk').count()
    def count_following(self):
        return self.follows.values('pk').count()
    def count_followers(self):
        return self.profile.follows
    def count_blacklist(self):
        return self.user_blocks.values('pk').count()
    def count_goods(self):
        return self.profile.goods
    def count_photos(self):
        return self.profile.photos
    def count_docs(self):
        return self.profile.docs
    def count_posts(self):
        return self.profile.posts
    def count_articles(self):
        return self.profile.articles
    def count_communities(self):
        return self.profile.communities
    def count_communities_ru(self):
        count = self.count_communities()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " сообщество"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " сообщества"
        else:
            return str(count) + " сообществ"
    def count_tracks(self):
        return self.profile.tracks
    def count_videos(self):
        return self.profile.videos
    def count_friends(self):
        return self.profile.friends

    def plus_photos(self, count):
        self.profile.photos += count
        return self.profile.save(update_fields=['photos'])
    def minus_photos(self, count):
        try:
            self.profile.photos -= count
            return self.profile.save(update_fields=['photos'])
        except:
            pass
    def plus_goods(self, count):
        self.profile.goods += count
        return self.profile.save(update_fields=['goods'])
    def minus_goods(self, count):
        try:
            self.profile.goods -= count
            return self.profile.save(update_fields=['goods'])
        except:
            pass
    def plus_posts(self, count):
        self.profile.posts += count
        return self.profile.save(update_fields=['posts'])
    def minus_posts(self, count):
        try:
            self.profile.posts -= count
            return self.profile.save(update_fields=['posts'])
        except:
            pass
    def plus_videos(self, count):
        self.profile.videos += count
        return self.profile.save(update_fields=['videos'])
    def minus_videos(self, count):
        try:
            self.profile.videos -= count
            return self.profile.save(update_fields=['videos'])
        except:
            pass
    def plus_docs(self, count):
        self.profile.docs += count
        return self.profile.save(update_fields=['docs'])
    def minus_docs(self, count):
        try:
            self.profile.docs -= count
            return self.profile.save(update_fields=['docs'])
        except:
            pass
    def plus_tracks(self, count):
        self.profile.tracks += count
        return self.profile.save(update_fields=['tracks'])
    def minus_tracks(self, count):
        try:
            self.profile.tracks -= count
            return self.profile.save(update_fields=['tracks'])
        except:
            pass
    def plus_communities(self, count):
        self.profile.communities += count
        return self.profile.save(update_fields=['communities'])
    def minus_communities(self, count):
        try:
            self.profile.communities -= count
            return self.profile.save(update_fields=['communities'])
        except:
            pass
    def plus_articles(self, count):
        self.profile.articles += count
        return self.profile.save(update_fields=['articles'])
    def minus_articles(self, count):
        try:
            self.profile.articles -= count
            return self.profile.save(update_fields=['articles'])
        except:
            pass
    def plus_friends(self, count):
        self.profile.friends += count
        return self.profile.save(update_fields=['friends'])
    def minus_friends(self, count):
        try:
            self.profile.friends -= count
            return self.profile.save(update_fields=['friends'])
        except:
            pass
    def plus_follows(self, count):
        self.profile.follows += count
        return self.profile.save(update_fields=['follows'])
    def minus_follows(self, count):
        try:
            self.profile.follows -= count
            return self.profile.save(update_fields=['follows'])
        except:
            pass


    ''''' GET всякие  219-186 '''''
    def get_6_friends(self):
        return self.get_all_friends()[:6]

    def get_6_communities(self):
        from communities.models import Community
        return Community.objects.filter(memberships__user=self).order_by("-memberships__visited")[0:6]

    def get_communities(self):
        from communities.models import Community
        return Community.objects.filter(memberships__user_id=self.pk).order_by("-memberships__visited")

    def get_all_friends_ids(self):
        my_frends = self.connections.values('target_user_id')
        return [i['target_user_id'] for i in my_frends]

    def get_friend_and_friend_of_friend_ids(self):
        frends = self.get_all_friends()
        frends_ids = self.get_all_friends_ids()
        query = []
        for frend in frends:
            query = query + frend.get_all_friends_ids()
        query = query + frends_ids
        set_query = list(set(query))
        try:
            set_query.remove(self.pk)
        except:
            pass
        return set_query


    def get_all_friends(self):
        query = []
        for id in self.get_all_friends_ids():
            query.append(User.objects.get(id=id))
        return query

    def get_online_friends(self):
        frends, query = self.get_all_friends(), []
        for frend in frends:
            if frend.get_online():
                query += [frend,]
        return query

    def get_online_friends_count(self):
        return len(self.get_all_friends())

    def get_6_online_friends(self):
        return self.get_online_friends()[:6]

    def get_draft_posts(self):
        from posts.models import Post
        return Post.objects.filter(creator_id=self.id, type=Post.C_OFFER, community__isnull=True)

    def get_draft_posts_of_community_with_pk(self, community_pk):
        from posts.models import Post
        return Post.objects.filter(creator_id=self.id, community_id=community_pk, type=Post.C_OFFER)

    def get_selected_post_list_pk(self):
        from users.model.list import UserPostsListPosition
        list = UserPostsListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_post_list().pk
    def get_selected_photo_list_pk(self):
        from users.model.list import UserPhotoListPosition
        list = UserPhotoListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_photo_list().pk
    def get_selected_doc_list_pk(self):
        from users.model.list import UserDocsListPosition
        list = UserDocsListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_doc_list().pk
    def get_selected_good_list_pk(self):
        from users.model.list import UserGoodListPosition
        list = UserGoodListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_good_list().pk
    def get_selected_music_list_pk(self):
        from users.model.list import UserPlayListPosition
        list = UserPlayListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_playlist().pk
    def get_selected_video_list_pk(self):
        from users.model.list import UserVideoListPosition
        list = UserVideoListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_video_list().pk
    def get_selected_survey_list_pk(self):
        from users.model.list import UserSurveyListPosition
        list = UserSurveyListPosition.objects.filter(user=self.pk, type=1).first()
        if list:
            return list.list
        else:
            return self.get_survey_list().pk

    def get_post_lists(self):
        from posts.models import PostsList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return PostsList.objects.filter(query)
    def get_post_lists_from_staffed_comunities(self):
        from posts.models import PostsList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return PostsList.objects.filter(query)

    def get_survey_lists(self):
        from survey.models import SurveyList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return SurveyList.objects.filter(query)
    def get_survey_lists_from_staffed_comunities(self):
        from survey.models import SurveyList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return SurveyList.objects.filter(query)

    def get_post_categories(self):
        from posts.models import PostCategory
        return PostCategory.objects.only("pk")

    def get_photo_lists(self):
        from gallery.models import PhotoList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return PhotoList.objects.filter(query)
    def get_photo_lists_from_staffed_comunities(self):
        from gallery.models import PhotoList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return PhotoList.objects.filter(query)

    def get_video_lists(self):
        from video.models import VideoList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return VideoList.objects.filter(query)
    def get_video_lists_from_staffed_comunities(self):
        from video.models import VideoList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return VideoList.objects.filter(query)

    def get_music_lists(self):
        from music.models import MusicList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return MusicList.objects.filter(query)
    def get_music_lists_from_staffed_comunities(self):
        from music.models import MusicList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return MusicList.objects.filter(query)

    def get_good_lists(self):
        from goods.models import GoodList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return GoodList.objects.filter(query)
    def get_good_lists_from_staffed_comunities(self):
        from good.models import GoodList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return GoodList.objects.filter(query)

    def get_survey_lists(self):
        from survey.models import SurveyList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return SurveyList.objects.filter(query)

    def get_doc_lists(self):
        from docs.models import DocsList
        return DocsList.objects.filter(creator_id=self.id, community__isnull=True).exclude(type__contains="_")
    def get_doc_lists_from_staffed_comunities(self):
        from docs.models import DocsList
        query = Q(community__in=self.get_staffed_communities())
        query.add(~Q(type__contains="_"), Q.AND)
        return DocsList.objects.filter(query)

    def get_good_list(self):
        from goods.models import GoodList
        return GoodList.objects.get(creator_id=self.pk, community__isnull=True, type="MAI")
    def get_playlist(self):
        from music.models import MusicList
        return MusicList.objects.get(creator_id=self.pk, community__isnull=True, type=MusicList.MAIN)
    def get_video_list(self):
        from video.models import VideoList
        return VideoList.objects.get(creator_id=self.pk, community__isnull=True, type=VideoList.MAIN)
    def get_photo_list(self):
        from gallery.models import PhotoList
        return PhotoList.objects.get(creator_id=self.pk, community__isnull=True, type=PhotoList.MAIN)

    def get_avatar_pk(self):
        from gallery.models import PhotoList
        try:
            list = PhotoList.objects.get(creator_id=self.pk, community__isnull=True, type=PhotoList.AVATAR)
            return list.get_items().first().pk
        except:
            return None
    def get_post_list(self):
        from posts.models import PostsList
        return PostsList.objects.get(creator_id=self.pk, community__isnull=True, type__contains="MA")
    def get_doc_list(self):
        from docs.models import DocsList
        return DocsList.objects.get(creator_id=self.pk, community__isnull=True, type__contains="MA")
    def get_survey_list(self):
        from survey.models import SurveyList
        return SurveyList.objects.get(creator_id=self.pk, community__isnull=True, type__contains="MA")
    def get_playlists(self):
        from music.models import MusicList
        return MusicList.objects.filter(creator_id=self.id, community__isnull=True, type__contains="MA")

    def get_6_photos(self):
        from gallery.models import Photo
        return Photo.objects.filter(creator_id=self.pk, community__isnull=True, type="PUB")[:6]
    def get_6_docs(self):
        from docs.models import Doc
        return Doc.objects.filter(creator_id=self.pk, community__isnull=True, type="PUB")[:6]
    def get_6_tracks(self):
        from music.models import Music
        return Music.objects.filter(creator_id=self.pk, community__isnull=True, type="PUB")[:6]
    def get_2_videos(self):
        from video.models import Video
        return Video.objects.filter(creator_id=self.pk, community__isnull=True, type="PUB")[:2]
    def get_3_goods(self):
        from goods.models import Good
        return Good.objects.filter(creator_id=self.pk, community__isnull=True, type="PUB")[:3]

    def get_music_count(self):
        return self.profile.tracks

    def get_last_music(self):
        return self.get_playlist().get_items()[:6]

    def get_video_count(self):
        return self.profile.videos

    def get_last_video(self):
        return self.get_video_list().get_items()[:2]

    def my_playlist_too(self):
        from music.models import MusicList, UserTempMusicList, SoundGenres

        if UserTempMusicList.objects.filter(user_id=self.pk).exists():
            temp_list = UserTempMusicList.objects.get(user_id=self.pk)
        else:
            return self.get_playlist().get_items()
        try:
            return MusicList.objects.get(pk=temp_list.list.pk).get_items()
        except:
            pass
        try:
            return SoundGenres.objects.get(pk=temp_list.genre.pk).get_items()
        except:
            pass

    def get_docs_count(self):
        return self.profile.docs

    def get_last_docs(self):
        return self.get_doc_list().get_items()[:6]

    def get_followers(self):
        query = Q(follows__followed_user_id=self.pk)
        query.add(~Q(type__contains="_"), Q.AND)
        return User.objects.filter(query)

    def get_all_users(self):
        query = ~Q(type__contains="_")
        if self.is_child():
            query.add(~Q(Q(type=User.VERIFIED_SEND)|Q(type=User.STANDART)), Q.AND)
        return User.objects.filter(query)

    def get_pop_followers(self):
        query = Q(follows__followed_user_id=self.pk)
        query.add(~Q(type__contains="_"), Q.AND)
        return User.objects.filter(query)[0:6]

    def get_followings(self):
        query = Q(followers__user_id=self.pk)
        query.add(~Q(type__contains="_"), Q.AND)
        return User.objects.filter(query)

    def get_friends_and_followings_ids(self):
        my_frends = self.connections.values('target_user_id')
        my_followings = self.followers.values('user_id')
        return [i['target_user_id'] for i in my_frends] + [u['user_id'] for u in my_followings]

    def get_common_friends_of_user(self, user):
        user = User.objects.get(pk=user.pk)
        if self.pk == user.pk:
            return ""
        my_frends = self.connections.values('target_user_id')
        user_frends = user.connections.values('target_user_id')
        result=list(set([i['target_user_id'] for i in my_frends]) & set([a['target_user_id'] for a in user_frends]))
        return User.objects.filter(id__in=result)

    def get_common_friends_of_community(self, community_id):
        from communities.models import Community

        community, my_frends = Community.objects.get(pk=community_id), self.connections.values('target_user_id')
        community_frends = community.memberships.values('user_id')
        result=list(set([i['target_user_id'] for i in my_frends]) & set([a['user_id'] for a in community_frends]))
        return User.objects.filter(id__in=result)

    def get_common_friends_of_community_count_ru(self, community_id):
        from communities.models import Community

        community = Community.objects.get(pk=community_id)
        my_frends = self.connections.values('target_user_id')
        community_frends = community.memberships.values('user_id')
        my_frends_ids = [i['target_user_id'] for i in my_frends]
        community_frends_ids = [i['user_id'] for i in community_frends]
        result=list(set(my_frends_ids) & set(community_frends_ids))
        count = User.objects.filter(id__in=result).values("pk").count()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " друг"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " друга"
        else:
            return str(count) + " друзей"

    def get_target_users(self):
        from stst.models import UserNumbers
        query = []
        for user in [i['target'] for i in UserNumbers.objects.filter(visitor=self.pk).values('target').order_by("-count")]:
            query = query + [User.objects.get(id=user)]
        return query

    def get_last_visited_communities(self):
        from stst.models import CommunityNumbers
        from communities.models import Community
        v_s = CommunityNumbers.objects.filter(user=self.pk).values('community')
        result = list()
        map(lambda x: not x in result and result.append(x), [i['community'] for i in v_s])
        query = []
        for i in result:
            query = query + [Community.objects.get(id=i), ]
        return query

    def get_visited_communities(self):
        from stst.models import CommunityNumbers
        from communities.models import Community
        v_s = CommunityNumbers.objects.filter(user=self.pk).distinct("community").values("community")
        return Community.objects.filter(id__in=[use['community'] for use in v_s])

    def get_visited_communities_count(self):
        from stst.models import CommunityNumbers
        return CommunityNumbers.objects.filter(user=self.pk).distinct("community").values("community").count()


    def join_community(self, community):
        from communities.models import Community
        from follows.models import CommunityFollow
        from invitations.models import CommunityInvite

        check_can_join_community(user=self, community_id=community.pk)
        community_to_join = Community.objects.get(pk=community.pk)
        community_to_join.add_member(self)
        if community_to_join.is_private():
            CommunityInvite.objects.filter(community_pk=community.pk, invited_user__id=self.id).delete()
        elif community_to_join.is_closed():
            CommunityFollow.objects.filter(community__pk=community.pk, user__id=self.id).delete()
        self.remove_featured_communities_from_all_list(community_to_join.pk)
        return community_to_join

    def add_news_subscriber_in_main_list(self, user_id):
        from users.model.list import ListUC, NewsUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        if not NewsUC.objects.filter(list=list, owner=self.pk, user=user_id).exists():
            NewsUC.objects.create(list=list, owner=self.pk, user=user_id)
    def delete_news_subscriber_from_main_list(self, user_id):
        from users.model.list import ListUC, NewsUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        if NewsUC.objects.filter(list=list, owner=self.pk, user=user_id).exists():
            notify = NewsUC.objects.get(list=list, owner=self.pk, user=user_id)
            notify.delete()
    def add_news_subscriber_in_list(self, user_id, list_id):
        from users.model.list import ListUC, NewsUC
        if not NewsUC.objects.filter(list_id=list_id, owner=self.pk, user=user_id).exists():
            NewsUC.objects.create(list_id=list_id, owner=self.pk, user=user_id)
    def delete_news_subscriber_from_list(self, user_id, list_id):
        from users.model.list import ListUC, NewsUC
        if NewsUC.objects.filter(list_id=list_id, owner=self.pk, user=user_id).exists():
            notify = NewsUC.objects.get(list_id=list_id, owner=self.pk, user=user_id)
            notify.delete()

    def add_notify_subscriber_in_main_list(self, user_id):
        from users.model.list import ListUC, NotifyUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        if not NotifyUC.objects.filter(list=list, owner=self.pk, user=user_id).exists():
            NotifyUC.objects.create(list=list, owner=self.pk, user=user_id)
    def delete_notify_subscriber_from_main_list(self, user_id):
        from users.model.list import ListUC, NotifyUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        if NotifyUC.objects.filter(list=list, owner=self.pk, user=user_id).exists():
            notify = NotifyUC.objects.get(list=list, owner=self.pk, user=user_id)
            notify.delete()
    def add_notify_subscriber_in_list(self, user_id, list_id):
        from users.model.list import ListUC, NotifyUC
        if not NotifyUC.objects.filter(list_id=list_id, owner=self.pk, user=user_id).exists():
            NotifyUC.objects.create(list_id=list_id, owner=self.pk, user=user_id)
    def delete_notify_subscriber_from_list(self, user_id, list_id):
        from users.model.list import ListUC, NotifyUC
        if NotifyUC.objects.filter(list_id=list_id, owner=self.pk, user=user_id).exists():
            notify = NotifyUC.objects.get(list_id=list_id, owner=self.pk, user=user_id)
            notify.delete()

    def get_user_main_news_ids(self):
        from users.model.list import ListUC, NewsUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        return [i['user'] for i in NewsUC.objects.filter(list_id=list.id, owner=self.pk, community=0, mute=False).values('user')]
    def get_community_main_news_ids(self):
        from users.model.list import ListUC, NewsUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        return [i['community'] for i in NewsUC.objects.filter(list_id=list.id, owner=self.pk, user=0, mute=False).values('community')]

    def get_user_main_notify_ids(self):
        from users.model.list import ListUC, NotifyUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        return [i['user'] for i in NotifyUC.objects.filter(list_id=list.id, owner=self.pk, community=0, mute=False).values('user')]
    def get_community_main_notify_ids(self):
        from users.model.list import ListUC, NotifyUC
        list = ListUC.objects.get(owner=self.pk, type=1)
        return [i['community'] for i in NotifyUC.objects.filter(list_id=list.id, owner=self.pk, user=0, mute=False).values('community')]

    def leave_community(self, community):
        check_can_leave_community(user=self, community_id=community.pk)
        return community.remove_member(self)

    def get_sity_count(self, sity):
        from stst.models import UserNumbers
        from users.model.profile import UserLocation

        v_s = UserNumbers.objects.filter(target=self.pk).values('target')
        return UserLocation.objects.filter(user_id__in=[use['target'] for use in v_s], city_ru=sity).count()

    def get_post_views_for_year(self, year):
        from posts.models import Post
        count, posts = 0, Post.objects.filter(creator_id=self.pk, created__year=year)
        for i in posts:
            count += i.view
        return count
    def get_post_views_for_month(self, month):
        from posts.models import Post
        count, posts = 0, Post.objects.filter(creator_id=self.pk, created__month=month)
        for i in posts:
            count += i.view
        return count
    def get_post_views_for_week(self, week):
        from posts.models import Post
        count, posts = 0, Post.objects.filter(creator_id=self.pk, created__day__in=week)
        for i in posts:
            count += i.view
        return count
    def get_post_views_for_day(self, day):
        from posts.models import Post
        count, posts = 0, Post.objects.filter(creator_id=self.pk, created__day=day)
        for i in posts:
            count += i.view
        return count

    def get_longest_penalties(self):
        return ModerationPenalty.objects.filter(type="USE", object_id=self.pk)[0].get_expiration()
    def get_moderated_description(self):
        from managers.models import Moderated
        obj = Moderated.objects.filter(type="USE", object_id=self.pk)[0]
        if obj.description:
            return obj.description
        else:
            return "Предупреждение за нарушение правил соцсети трезвый.рус"
    ''''' начало сообщения '''''

    def get_private_chats(self):
        from chat.models import Chat
        return Chat.objects.filter(chat_relation__user_id=self.pk, chat_relation__type="ACT", type=Chat.PRIVATE)

    def get_all_chats(self):
        from chat.models import Chat
        query = Q(chat_relation__user_id=self.pk, chat_relation__type="ACT")
        query.add(~Q(type__contains="_"), Q.AND)
        chats = Chat.objects.filter(query)
        list = []
        for chat in chats:
            if chat.is_public() or chat.is_group():
                list.append(chat)
            elif chat.is_not_empty(self.pk):
                list.append(chat)
        return list

    def get_chats_and_friends(self):
        from itertools import chain
        return list(chain(self.get_all_chats(), self.get_all_friends()))

    def is_administrator_of_chat(self, chat_pk):
        return self.chat_users.filter(chat__pk=chat_pk, is_administrator=True, type="ACT").exists()
    def is_member_of_chat(self, chat_pk):
        return self.chat_users.filter(chat__pk=chat_pk, type="ACT").exists()

    def get_unread_chats(self):
        chats, count = self.get_all_chats(), 0
        for chat in chats:
            if chat.chat_message.filter(unread=True).exclude(creator_id=self.pk).exists():
                count += 1
        if count > 0:
            return count
        else:
            return ''

    def get_user_notify(self):
        from notify.models import Notify

        query = Q(creator_id__in=self.get_user_main_notify_ids())| \
                Q(community_id__in=self.get_community_profile_notify_ids())
        query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
        return Notify.objects.only('created').filter(query)

    def read_user_notify(self):
        from notify.models import Notify
        Notify.u_notify_unread(self.pk)

    def count_user_unread_notify(self):
        from notify.models import Notify
        query = Q(recipient_id=self.pk, community__isnull=True, status="U")
        return Notify.objects.filter(query).values("pk").count()

    def unread_notify_count(self):
        count = self.count_user_unread_notify()
        if self.is_staffed_user():
            for community in self.get_staffed_communities():
                count += community.count_community_unread_notify(self.pk)
        if count > 0:
            return count
        else:
            return ''

    def unread_profile_notify_count(self):
        count = self.count_user_unread_notify()
        if count > 0:
            return '<span class="tab_badge badge-success" style="font-size: 60%;">' + str(count) + '</span>'
        else:
            return ''

    def get_member_for_notify_ids(self):
        from users.model.list import NotifyUC
        recipients = NotifyUC.objects.filter(owner=self.pk, community=0).values("user")
        return [i['user'] for i in recipients]


    def is_user_can_see_info(self, user_id):
        private = self.profile_private
        if private.can_see_info == 1:
            return True
        elif private.can_see_info == 6 and self.pk == user_pk:
            return True
        elif private.can_see_info == 4 and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_info == 5 and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_info == 17:
            return not user_pk in self.get_can_see_info_exclude_users_ids()
        elif private.can_see_info == 18:
            return user_pk in self.get_can_see_info_include_users_ids()
        return False

    def is_user_can_add_in_chat(self, user_pk):
        """ Немного поменяем поведение проверки на приватность добавления пользователя в чат.
            Если выбрано YOU, мы подразумеваем "Только я", а это в данном случае НИКТО.
            Потому вернем False, если выбран этот пункт.
         """
        private = self.profile_private
        if private.can_add_in_chat == 1:
            return True
        elif private.can_add_in_chat == 6:
            return False
        elif private.can_add_in_chat == 4 and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_add_in_chat == 5 and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_add_in_chat == 17:
            return not user_pk in self.get_can_add_in_chat_exclude_users_ids()
        elif private.can_add_in_chat == 18:
            return user_pk in self.get_can_add_in_chat_include_users_ids()
        return False

    def is_user_can_see_post(self, user_pk):
        private = self.profile_private
        if private.can_see_post == 1:
            return True
        elif private.can_see_post == 6 and self.pk == user_pk:
            return True
        elif private.can_see_post == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_post == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_post == 17:
            return not user_pk in self.get_can_see_post_exclude_users_ids()
        elif private.can_see_post == 18:
            return user_pk in self.get_can_see_post_include_users_ids()
        return False

    def is_user_can_see_community(self, user_pk):
        private = self.profile_private
        if private.can_see_community == 1:
            return True
        elif private.can_see_community == 6 and self.pk == user_pk:
            return True
        elif private.can_see_community == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_community == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_community == 17:
            return not user_pk in self.get_can_see_community_exclude_users_ids()
        elif private.can_see_community == 18:
            return user_pk in self.get_can_see_community_include_users_ids()
        return False

    def is_user_can_see_photo(self, user_pk):
        private = self.profile_private
        if private.can_see_photo == 1:
            return True
        elif private.can_see_photo == 6 and self.pk == user_pk:
            return True
        elif private.can_see_photo == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_photo == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_photo == 17:
            return not user_pk in self.get_can_see_photo_exclude_users_ids()
        elif private.can_see_photo == 18:
            return user_pk in self.get_can_see_photo_include_users_ids()
        return False

    def is_user_can_see_video(self, user_pk):
        private = self.profile_private
        if private.can_see_video == 1:
            return True
        elif private.can_see_video == 6 and self.pk == user_pk:
            return True
        elif private.can_see_video == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_video == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_video == 17:
            return not user_pk in self.get_can_see_video_exclude_users_ids()
        elif private.can_see_video == 18:
            return user_pk in self.get_can_see_video_include_users_ids()
        return False

    def is_user_can_see_music(self, user_pk):
        private = self.profile_private
        if private.can_see_music == 1:
            return True
        elif private.can_see_music == 6 and self.pk == user_pk:
            return True
        elif private.can_see_music == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_music == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_music == 17:
            return not user_pk in self.get_can_see_music_exclude_users_ids()
        elif private.can_see_music == 18:
            return user_pk in self.get_can_see_music_include_users_ids()
        return False

    def is_user_can_see_doc(self, user_pk):
        private = self.profile_private
        if private.can_see_doc == 1:
            return True
        elif private.can_see_doc == 6 and self.pk == user_pk:
            return True
        elif private.can_see_doc == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_doc == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_doc == 17:
            return not user_pk in self.get_can_see_doc_exclude_users_ids()
        elif private.can_see_doc == 18:
            return user_pk in self.get_can_see_doc_include_users_ids()
        return False

    def is_user_can_see_friend(self, user_pk):
        private = self.profile_private
        if private.can_see_friend == 1:
            return True
        elif private.can_see_friend == 6 and self.pk == user_pk:
            return True
        elif private.can_see_friend == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_friend == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_friend == 17:
            return not user_pk in self.get_can_see_friend_exclude_users_ids()
        elif private.can_see_friend == 18:
            return user_pk in self.get_can_see_friend_include_users_ids()
        return False

    def is_user_can_see_good(self, user_pk):
        private = self.profile_private
        if private.can_see_good == 1:
            return True
        elif private.can_see_good == 6 and self.pk == user_pk:
            return True
        elif private.can_see_good == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_good == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_good == 17:
            return not user_pk in self.get_can_see_good_exclude_users_ids()
        elif private.can_see_good == 18:
            return user_pk in self.get_can_see_good_include_users_ids()
        return False
    def is_user_can_see_survey(self, user_pk):
        private = self.profile_private
        if private.can_see_survey == 1:
            return True
        elif private.can_see_survey == 6 and self.pk == user_pk:
            return True
        elif private.can_see_survey == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_see_survey == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_survey == 17:
            return not user_pk in self.get_can_see_survey_exclude_users_ids()
        elif private.can_see_survey == 18:
            return user_pk in self.get_can_see_survey_include_users_ids()
        return False
    def is_user_can_send_message(self, user_pk):
        private = self.profile_private
        if private.can_send_message == 1:
            return True
        elif private.can_send_message == 6 and self.pk == user_pk:
            return True
        elif private.can_send_message == private.FRIENDS and user_pk in self.get_all_friends_ids():
            return True
        elif private.can_send_message == private.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_send_message == 17:
            return not user_pk in self.get_can_send_message_exclude_users_ids()
        elif private.can_send_message == 18:
            return user_pk in self.get_can_send_message_include_users_ids()
        return False

    def is_anon_user_can_see_post(self):
        private = self.profile_private
        return private.can_see_post == 1
    def is_anon_user_can_see_photo(self):
        private = self.profile_private
        return private.can_see_photo == 1
    def is_anon_user_can_see_community(self):
        private = self.profile_private
        return private.can_see_community == 1
    def is_anon_user_can_see_friend(self):
        private = self.profile_private
        return private.can_see_friend == 1
    def is_anon_user_can_see_doc(self):
        private = self.profile_private
        return private.can_see_doc == 1
    def is_anon_user_can_see_music(self):
        private = self.profile_private
        return private.can_see_music == 1
    def is_anon_user_can_see_video(self):
        private = self.profile_private
        return private.can_see_video == 1
    def is_anon_user_can_see_good(self):
        private = self.profile_private
        return private.can_see_good == 1

    def post_exclude_users(self, users, type):
        from frends.models import ConnectPerm

        private = self.profile_private
        if type == "can_see_community":
            list = self.connections.filter(connect_ie_settings__can_see_community=2)
            for i in list:
                i.connect_ie_settings.can_see_community = 0
                i.connect_ie_settings.save(update_fields=["can_see_community"])
            for user_id in users:
                friend = self.connections.filter(user_id=self.pk,target_user_id=user_id).first()
                try:
                    perm = friend.connect_ie_settings
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_community = 2
                perm.save(update_fields=["can_see_community"])
            private.can_see_community = 17
            private.save(update_fields=["can_see_community"])
        elif type == "can_see_info":
            list = self.connections.filter(connect_ie_settings__can_see_info=2)
            for i in list:
                i.connect_ie_settings.can_see_info = 0
                i.connect_ie_settings.save(update_fields=["can_see_info"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_info = 2
                perm.save(update_fields=["can_see_info"])
            private.can_see_info = 17
            private.save(update_fields=["can_see_info"])
        elif type == "can_see_friend":
            list = self.connections.filter(connect_ie_settings__can_see_friend=2)
            for i in list:
                i.connect_ie_settings.can_see_friend = 0
                i.connect_ie_settings.save(update_fields=["can_see_friend"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_friend = 2
                perm.save(update_fields=["can_see_friend"])
            private.can_see_friend = 17
            private.save(update_fields=["can_see_friend"])
        elif type == "can_send_message":
            list = self.connections.filter(connect_ie_settings__can_send_message=2)
            for i in list:
                i.connect_ie_settings.can_send_message = 0
                i.connect_ie_settings.save(update_fields=["can_send_message"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_send_message = 2
                perm.save(update_fields=["can_send_message"])
            private.can_send_message = 17
            private.save(update_fields=["can_send_message"])
        elif type == "can_add_in_chat":
            list = self.connections.filter(connect_ie_settings__can_add_in_chat=2)
            for i in list:
                i.connect_ie_settings.can_add_in_chat = 0
                i.connect_ie_settings.save(update_fields=["can_add_in_chat"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_add_in_chat = 2
                perm.save(update_fields=["can_add_in_chat"])
            private.can_add_in_chat = 17
            private.save(update_fields=["can_add_in_chat"])
        elif type == "can_see_post":
            list = self.connections.filter(connect_ie_settings__can_see_post=2)
            for i in list:
                i.connect_ie_settings.can_see_post = 0
                i.connect_ie_settings.save(update_fields=["can_see_post"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_post = 2
                perm.save(update_fields=["can_see_post"])
            private.can_see_post = 17
            private.save(update_fields=["can_see_post"])
        elif type == "can_see_photo":
            list = self.connections.filter(connect_ie_settings__can_see_photo=2)
            for i in list:
                i.connect_ie_settings.can_see_photo = 0
                i.connect_ie_settings.save(update_fields=["can_see_photo"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_photo = 2
                perm.save(update_fields=["can_see_photo"])
            private.can_see_photo = 17
            private.save(update_fields=["can_see_photo"])
        elif type == "can_see_good":
            list = self.connections.filter(connect_ie_settings__can_see_good=2)
            for i in list:
                i.connect_ie_settings.can_see_good = 0
                i.connect_ie_settings.save(update_fields=["can_see_good"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_good = 2
                perm.save(update_fields=["can_see_good"])
            private.can_see_good = 17
            private.save(update_fields=["can_see_good"])
        elif type == "can_see_video":
            list = self.connections.filter(connect_ie_settings__can_see_video=2)
            for i in list:
                i.connect_ie_settings.can_see_video = 0
                i.connect_ie_settings.save(update_fields=["can_see_video"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_video = 2
                perm.save(update_fields=["can_see_video"])
            private.can_see_video = 17
            private.save(update_fields=["can_see_video"])
        elif type == "can_see_music":
            list = self.connections.filter(connect_ie_settings__can_see_music=2)
            for i in list:
                i.connect_ie_settings.can_see_music = 0
                i.connect_ie_settings.save(update_fields=["can_see_music"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_music = 2
                perm.save(update_fields=["can_see_music"])
            private.can_see_music = 17
            private.save(update_fields=["can_see_music"])
        elif type == "can_see_planner":
            list = self.connections.filter(connect_ie_settings__can_see_planner=2)
            for i in list:
                i.connect_ie_settings.can_see_planner = 0
                i.connect_ie_settings.save(update_fields=["can_see_planner"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_planner = 2
                perm.save(update_fields=["can_see_planner"])
            private.can_see_planner = 17
            private.save(update_fields=["can_see_planner"])
        elif type == "can_see_doc":
            list = self.connections.filter(connect_ie_settings__can_see_doc=2)
            for i in list:
                i.connect_ie_settings.can_see_doc = 0
                i.connect_ie_settings.save(update_fields=["can_see_doc"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_doc = 2
                perm.save(update_fields=["can_see_doc"])
            private.can_see_doc = 17
            private.save(update_fields=["can_see_doc"])

    def post_include_users(self, users, type):
        from frends.models import ConnectPerm

        private = self.profile_private
        if type == "can_see_community":
            list = self.connections.filter(connect_ie_settings__can_see_community=1)
            for i in list:
                i.connect_ie_settings.can_see_community = 0
                i.connect_ie_settings.save(update_fields=["can_see_community"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_community = 1
                perm.save(update_fields=["can_see_community"])
            private.can_see_community = 18
            private.save(update_fields=["can_see_community"])
        elif type == "can_see_info":
            list = self.connections.filter(connect_ie_settings__can_see_info=1)
            for i in list:
                i.connect_ie_settings.can_see_info = 0
                i.connect_ie_settings.save(update_fields=["can_see_info"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_info = 1
                perm.save(update_fields=["can_see_info"])
            private.can_see_info = 18
            private.save(update_fields=["can_see_info"])
        elif type == "can_see_friend":
            list = self.connections.filter(connect_ie_settings__can_see_friend=1)
            for i in list:
                i.connect_ie_settings.can_see_friend = 0
                i.connect_ie_settings.save(update_fields=["can_see_friend"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_friend = 1
                perm.save(update_fields=["can_see_friend"])
            private.can_see_friend = 18
            private.save(update_fields=["can_see_friend"])
        elif type == "can_send_message":
            list = self.connections.filter(connect_ie_settings__can_send_message=1)
            for i in list:
                i.connect_ie_settings.can_send_message = 0
                i.connect_ie_settings.save(update_fields=["can_send_message"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_send_message = 1
                perm.save(update_fields=["can_send_message"])
            private.can_send_message = 18
            private.save(update_fields=["can_send_message"])
        elif type == "can_add_in_chat":
            list = self.connections.filter(connect_ie_settings__can_add_in_chat=1)
            for i in list:
                i.connect_ie_settings.can_add_in_chat = 0
                i.connect_ie_settings.save(update_fields=["can_add_in_chat"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_add_in_chat = 1
                perm.save(update_fields=["can_add_in_chat"])
            private.can_add_in_chat = 18
            private.save(update_fields=["can_add_in_chat"])
        elif type == "can_see_post":
            list = self.connections.filter(connect_ie_settings__can_see_post=1)
            for i in list:
                i.connect_ie_settings.can_see_post = 0
                i.connect_ie_settings.save(update_fields=["can_see_post"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_post = 1
                perm.save(update_fields=["can_see_post"])
            private.can_see_post = 18
            private.save(update_fields=["can_see_post"])
        elif type == "can_see_photo":
            list = self.connections.filter(connect_ie_settings__can_see_photo=1)
            for i in list:
                i.connect_ie_settings.can_see_photo = 0
                i.connect_ie_settings.save(update_fields=["can_see_photo"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_photo = 1
                perm.save(update_fields=["can_see_photo"])
            private.can_see_photo = 18
            private.save(update_fields=["can_see_photo"])
        elif type == "can_see_good":
            list = self.connections.filter(connect_ie_settings__can_see_good=1)
            for i in list:
                i.connect_ie_settings.can_see_good = 0
                i.connect_ie_settings.save(update_fields=["can_see_good"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_good = 1
                perm.save(update_fields=["can_see_good"])
            private.can_see_good = 18
            private.save(update_fields=["can_see_good"])
        elif type == "can_see_video":
            list = self.connections.filter(connect_ie_settings__can_see_video=1)
            for i in list:
                i.connect_ie_settings.can_see_video = 0
                i.connect_ie_settings.save(update_fields=["can_see_video"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_video = 1
                perm.save(update_fields=["can_see_video"])
            private.can_see_video = 18
            private.save(update_fields=["can_see_video"])
        elif type == "can_see_music":
            list = self.connections.filter(connect_ie_settings__can_see_music=1)
            for i in list:
                i.connect_ie_settings.can_see_music = 0
                i.connect_ie_settings.save(update_fields=["can_see_music"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_music = 1
                perm.save(update_fields=["can_see_music"])
            private.can_see_music = 18
            private.save(update_fields=["can_see_music"])
        elif type == "can_see_planner":
            list = self.connections.filter(connect_ie_settings__can_see_planner=1)
            for i in list:
                i.connect_ie_settings.can_see_planner = 0
                i.connect_ie_settings.save(update_fields=["can_see_planner"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_planner = 1
                perm.save(update_fields=["can_see_planner"])
            private.can_see_planner = 18
            private.save(update_fields=["can_see_planner"])
        elif type == "can_see_doc":
            list = self.connections.filter(connect_ie_settings__can_see_doc=1)
            for i in list:
                i.connect_ie_settings.can_see_doc = 0
                i.connect_ie_settings.save(update_fields=["can_see_doc"])
            for user_id in users:
                friend = self.connections.filter(target_user_id=user_id).first()
                try:
                    perm = ConnectPerm.objects.get(user_id=friend.pk)
                except:
                    perm = ConnectPerm.objects.create(user_id=friend.pk)
                perm.can_see_doc = 1
                perm.save(update_fields=["can_see_doc"])
            private.can_see_doc = 18
            private.save(update_fields=["can_see_doc"])


    def get_can_see_community_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_community=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_community_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_community=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_community_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_community_exclude_users_ids())
    def get_can_see_community_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_community_include_users_ids())

    def get_can_see_info_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_info=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_info_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_info=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_info_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_info_exclude_users_ids())
    def get_can_see_info_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_info_include_users_ids())

    def get_can_see_friend_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_friend=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_friend_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_friend=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_friend_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_friend_exclude_users_ids())
    def get_can_see_friend_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_friend_include_users_ids())

    def get_can_send_message_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_send_message=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_send_message_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_send_message=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_send_message_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_send_message_exclude_users_ids())
    def get_can_send_message_include_users(self):
        return User.objects.filter(id__in=self.get_can_send_message_include_users_ids())

    def get_can_add_in_chat_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_add_in_chat=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_add_in_chat_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_add_in_chat=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_add_in_chat_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_add_in_chat_exclude_users_ids())
    def get_can_add_in_chat_include_users(self):
        return User.objects.filter(id__in=self.get_can_add_in_chat_include_users_ids())

    def get_can_see_post_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_post=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_post_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_post=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_post_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_post_exclude_users_ids())
    def get_can_see_post_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_post_include_users_ids())

    def get_can_see_photo_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_photo=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_photo_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_photo=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_photo_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_photo_exclude_users_ids())
    def get_can_see_photo_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_photo_include_users_ids())

    def get_can_see_good_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_good=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_good_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_good=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_good_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_good_exclude_users_ids())
    def get_can_see_good_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_good_include_users_ids())

    def get_can_see_video_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_video=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_video_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_video=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_video_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_video_exclude_users_ids())
    def get_can_see_video_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_video_include_users_ids())

    def get_can_see_music_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_music=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_music_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_music=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_music_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_music_exclude_users_ids())
    def get_can_see_music_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_music_include_users_ids())

    def get_can_see_planner_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_planner=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_planner_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_planner=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_planner_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_planner_exclude_users_ids())
    def get_can_see_planner_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_planner_include_users_ids())

    def get_can_see_doc_exclude_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_doc=2).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_doc_include_users_ids(self):
        list = self.connections.filter(connect_ie_settings__can_see_doc=1).values("target_user_id")
        return [i['target_user_id'] for i in list]
    def get_can_see_doc_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_doc_exclude_users_ids())
    def get_can_see_doc_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_doc_include_users_ids())
