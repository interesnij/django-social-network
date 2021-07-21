import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from common.utils import try_except
from common.check.user import *
from users.helpers import upload_to_user_directory


class User(AbstractUser):
    PHONE_NO_VERIFIED,CHILD,PRIVATE_CHILD,STANDART,PRIVATE_STANDART,VERIFIED_SEND,PRIVATE_VERIFIED_SEND,VERIFIED,PRIVATE_VERIFIED,IDENTIFIED_SEND,PRIVATE_IDENTIFIED_SEND,IDENTIFIED,PRIVATE_IDENTIFIED,MANAGER,PRIVATE_MANAGER,SUPERMANAGER,PRIVATE_SUPERMANAGER = '_PV','CHI','CHIP','STA','STAP','VES','VESP','VER','VERP','IDS','IDSP','IDE','IDEP','MAN','MANP','SUPR','SUPRP'
    CLOSED_CHILD,CLOSED_PRIVATE_CHILD,CLOSED_STANDART,CLOSED_PRIVATE_STANDART,CLOSED_VERIFIED_SEND,CLOSED_PRIVATE_VERIFIED_SEND,CLOSED_VERIFIED,CLOSED_PRIVATE_VERIFIED,CLOSED_IDENTIFIED_SEND,CLOSED_PRIVATE_IDENTIFIED_SEND,CLOSED_IDENTIFIED,CLOSED_PRIVATE_IDENTIFIED,CLOSED_MANAGER,CLOSED_PRIVATE_MANAGER = '_CLOC','_CLOCP','_CLOS','_CLOSP','_CLOVS','_CLOVSP','_CLOV','_CLOVP','_CLOIS','_CLOISP','_CLOI','_CLOIP','_CLOM','_CLOMP'
    DELETED_CHILD,DELETED_PRIVATE_CHILD,DELETED_STANDART,DELETED_PRIVATE_STANDART,DELETED_VERIFIED_SEND,DELETED_PRIVATE_VERIFIED_SEND,DELETED_VERIFIED,DELETED_PRIVATE_VERIFIED,DELETED_IDENTIFIED_SEND,DELETED_PRIVATE_IDENTIFIED_SEND,DELETED_IDENTIFIED,DELETED_PRIVATE_IDENTIFIED,DELETED_MANAGER,DELETED_PRIVATE_MANAGER = '_DELC','_DELCP', '_DELS','_DELSP', '_DELVS','_DELVSP', '_DELV','_DELVP', '_DELIS','_DELISP', '_DELI','_DELIP', '_DELM','_DELMP'
    SUSPENDED_CHILD,SUSPENDED_PRIVATE_CHILD,SUSPENDED_STANDART,SUSPENDED_PRIVATE_STANDART,SUSPENDED_VERIFIED_SEND,SUSPENDED_PRIVATE_VERIFIED_SEND, SUSPENDED_VERIFIED,SUSPENDED_PRIVATE_VERIFIED, SUSPENDED_IDENTIFIED_SEND,SUSPENDED_PRIVATE_IDENTIFIED_SEND,SUSPENDED_IDENTIFIED,SUSPENDED_PRIVATE_IDENTIFIED,SUSPENDED_MANAGER,SUSPENDED_PRIVATE_MANAGER = '_SUSC','_SUSCP', '_SUSS','_SUSSP', '_SUSVS','_SUSVSP', '_SUSV','_SUSVP', '_SUSIS','_SUSISP', '_SUSI','_SUSIP', '_SUSM','_SUSMP'
    BANNER_CHILD,BANNER_PRIVATE_CHILD,BANNER_STANDART,BANNER_PRIVATE_STANDART,BANNER_VERIFIED_SEND,BANNER_PRIVATE_VERIFIED_SEND,BANNER_VERIFIED,BANNER_PRIVATE_VERIFIED,BANNER_IDENTIFIED_SEND,BANNER_PRIVATE_IDENTIFIED_SEND,BANNER_IDENTIFIED,BANNER_PRIVATE_IDENTIFIED,BANNER_MANAGER,BANNER_PRIVATE_MANAGER = '_BANC','_BANCP', '_BANS','_BANSP', '_BANVS','_BANVSP', '_BANV','_BANVP', '_BANIS','_BANISP', '_BANI','_BANIP', '_BANM','_BANMP'
    TYPE = (
        (CHILD, 'Ребенок'),(PRIVATE_CHILD, 'Ребенок приватный'),(PHONE_NO_VERIFIED, 'Телефон не подтвержден'),(STANDART, 'Обычные права'),(PRIVATE_STANDART, 'Обычный приватный'),(VERIFIED_SEND, 'Запрос на проверку'),(PRIVATE_VERIFIED_SEND, 'Запрос на проверку приватный'),(VERIFIED, 'Проверенный'),(PRIVATE_VERIFIED, 'Проверенный приватный'),(IDENTIFIED_SEND, 'Запрос на идентификацию'),(PRIVATE_IDENTIFIED_SEND, 'Запрос на идентификацию приватный'),(IDENTIFIED, 'Идентифицированный'),(PRIVATE_IDENTIFIED, 'Идентифицированный приватный'),(MANAGER, 'Менеджер'),(PRIVATE_MANAGER, 'Менеджер приватный'),(SUPERMANAGER, 'Суперменеджер'),(PRIVATE_SUPERMANAGER, 'Суперменеджер приватный'),
        (DELETED_CHILD, 'Удален ребенок'),(DELETED_PRIVATE_CHILD, 'Удален ребенок приватный'),(DELETED_STANDART, 'Удален'),(DELETED_PRIVATE_STANDART, 'Удален приватный'),(DELETED_VERIFIED_SEND, 'Удален подавший на верификацию'),(DELETED_PRIVATE_VERIFIED_SEND, 'Удален подавший на верификацию приватный'),(DELETED_VERIFIED, 'Удален верифицированный'),(DELETED_PRIVATE_VERIFIED, 'Удален верифицированный приватный'),(DELETED_IDENTIFIED_SEND, 'Удален подавший на идентификацию'),(DELETED_PRIVATE_IDENTIFIED_SEND, 'Удален подавший на идентификацию приватный'),(DELETED_IDENTIFIED, 'Удален идентифиированный'),(DELETED_PRIVATE_IDENTIFIED, 'Удален идентифиированный приватный'),(DELETED_MANAGER, 'Удален менеджер'),(DELETED_PRIVATE_MANAGER, 'Удален менеджер приватный'),
        (CLOSED_CHILD, 'Закрыт ребенок'),(CLOSED_PRIVATE_CHILD, 'Закрыт ребенок приватный'),(CLOSED_STANDART, 'Закрыт'),(CLOSED_PRIVATE_STANDART, 'Закрыт приватный'),(CLOSED_VERIFIED_SEND, 'Удален подавший на верификацию'),(CLOSED_PRIVATE_VERIFIED_SEND, 'Удален подавший на верификацию приватный'),(CLOSED_VERIFIED, 'Закрыт верифицированный'),(CLOSED_PRIVATE_VERIFIED, 'Закрыт верифицированный приватный'),(CLOSED_IDENTIFIED_SEND, 'Закрыт подавший на идентификацию'),(CLOSED_PRIVATE_IDENTIFIED_SEND, 'Закрыт подавший на идентификацию приватный'),(CLOSED_IDENTIFIED, 'Закрыт идентифиированный'),(CLOSED_PRIVATE_IDENTIFIED, 'Закрыт идентифиированный приватный'),(CLOSED_MANAGER, 'Закрыт менеджер'),(CLOSED_PRIVATE_MANAGER, 'Закрыт менеджер приватный'),
        (SUSPENDED_CHILD, 'Заморожен ребенок'),(SUSPENDED_PRIVATE_CHILD, 'Заморожен ребенок приватный'),(SUSPENDED_STANDART, 'Заморожен'),(SUSPENDED_PRIVATE_STANDART, 'Заморожен приватный'),(SUSPENDED_VERIFIED_SEND, 'Заморожен подавший на верификацию'),(SUSPENDED_PRIVATE_VERIFIED_SEND, 'Заморожен подавший на верификацию приватный'),(SUSPENDED_VERIFIED, 'Заморожен верифицированный'),(SUSPENDED_PRIVATE_VERIFIED, 'Заморожен верифицированный приватный'),(SUSPENDED_IDENTIFIED_SEND, 'Заморожен подавший на идентификацию'),(SUSPENDED_PRIVATE_IDENTIFIED_SEND, 'Заморожен подавший на идентификацию приватный'),(SUSPENDED_IDENTIFIED, 'Заморожен идентифиированный'),(SUSPENDED_PRIVATE_IDENTIFIED, 'Заморожен идентифиированный приватный'),(SUSPENDED_MANAGER, 'Заморожен менеджер'),(SUSPENDED_PRIVATE_MANAGER, 'Заморожен менеджер приватный'),
        (BANNER_CHILD, 'Баннер ребенок'),(BANNER_PRIVATE_CHILD, 'Баннер ребенок приватный'),(BANNER_STANDART, 'Баннер'),(BANNER_PRIVATE_STANDART, 'Баннер приватный'),(BANNER_VERIFIED_SEND, 'Баннер подавший на верификацию'),(BANNER_PRIVATE_VERIFIED_SEND, 'Баннер подавший на верификацию приватный'),(BANNER_VERIFIED, 'Баннер верифицированный'),(BANNER_PRIVATE_VERIFIED, 'Баннер верифицированный приватный'),(BANNER_IDENTIFIED_SEND, 'Баннер подавший на идентификацию'),(BANNER_PRIVATE_IDENTIFIED_SEND, 'Баннер подавший на идентификацию приватный'),(BANNER_IDENTIFIED, 'Баннер идентифиированный'),(BANNER_PRIVATE_IDENTIFIED, 'Баннер идентифиированный приватный'),(BANNER_MANAGER, 'Баннер менеджер'),(BANNER_PRIVATE_MANAGER, 'Баннер менеджер приватный'),
    )
    MALE, FEMALE, DESCTOP, PHONE = 'Man', 'Fem', 'De', 'Ph'
    GENDER = ((MALE, 'Мужской'),(FEMALE, 'Женский'),)
    DEVICE = ((DESCTOP, 'Комп'),(PHONE, 'Телефон'),)

    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, unique=True, verbose_name='Телефон')
    type = models.CharField(max_length=8, choices=TYPE, default=PHONE_NO_VERIFIED, verbose_name="Уровень доступа")
    gender = models.CharField(max_length=5, choices=GENDER, blank=True, verbose_name="Пол")
    device = models.CharField(max_length=5, choices=DEVICE, blank=True, verbose_name="Оборудование")
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    have_link = models.CharField(max_length=17, blank=True, verbose_name='Ссылка')
    sity = models.CharField(max_length=settings.PROFILE_LOCATION_MAX_LENGTH, blank=True, verbose_name="Местоположение")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    gender = models.CharField(max_length=5, choices=GENDER, blank=True, verbose_name="Пол")
    language = models.CharField(max_length=7, choices=settings.LANGUAGES, default="ru")
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()

    def is_closed_profile(self):
        return self.type[-1] == "P"

    def get_last_location(self):
        from users.model.profile import UserLocation
        return UserLocation.objects.filter(user=self)[0]

    def is_can_fixed_post(self):
        from posts.models import PostList
        try:
            list = PostList.objects.get(creator_id=self.pk, type=PostList.FIXED)
            return list.count_fix_items() < 10
        except:
            return None

    def get_verb_gender(self, verb):
        if self.is_women():
            return "W" + verb
        else:
            return verb

    def get_6_populate_friends(self):
        query = []
        for frend_id in self.get_6_populate_friends_ids():
            query.append(User.objects.get(pk=frend_id))
        return query

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
        query = []
        for sticker in UserPopulateStickers.objects.filter(user_id=self.pk)[:20]:
            query.append(Stickers.objects.get(id=sticker.pk))
        return query
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

    def is_suspended(self):
        return self.type[:4] == "_SUS"
    def is_have_warning_banner(self):
        return self.type[:4] == "_BAN"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_manager(self):
        return self.type == User.MANAGER
    def is_supermanager(self):
        return self.type == User.SUPERMANAGER
    def is_verified_send(self):
        return self.type == User.VERIFIED_SEND
    def is_verified(self):
        return self.type == User.VERIFIED
    def is_identified_send(self):
        return self.type == User.IDENTIFIED_SEND
    def is_identified(self):
        return self.type == User.IDENTIFIED
    def is_child(self):
        return self.type == User.CHILD
    def is_no_phone_verified(self):
        return self.type == User.PHONE_NO_VERIFIED
    def is_child_safety(self):
        if self.type == User.MANAGER or self.type == User.SUPERMANAGER or self.type == User.VERIFIED:
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
        self.save(update_fields=['b_avatar'])
        return self.save(update_fields=['b_avatar'])

    def get_b_avatar(self):
        try:
            return self.b_avatar.url
        except:
            return None

    def get_avatar(self):
        try:
            return self.s_avatar.url
        except:
            return None

    def get_s_avatar(self):
        if self.s_avatar:
            return '<img style="border-radius:30px;width:30px;" alt="image" src="' + self.s_avatar.url + '" />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_30" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'

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
        self.follow_user_with_id(user.pk)
        user.plus_follows(1)

    def follow_user_with_id(self, user_id):
        from follows.models import Follow

        check_can_follow_user(user_id=user_id, user=self)
        if self.pk == user_id:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        elif not self.is_closed_profile():
            self.add_news_subscriber(user_id)
        return Follow.create_follow(user_id=self.pk, followed_user_id=user_id)

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

    def get_or_create_possible_friend(self, user):
        from users.model.list import UserFeaturedFriend

        if self.pk != user.pk and not UserFeaturedFriend.objects.filter(user=self.pk, featured_user=user.pk).exists() \
            and not self.is_connected_with_user_with_id(user_id=user.pk) and not self.is_blocked_with_user_with_id(user_id=user.pk):
            #and not (self.is_child() and not user.is_child_safety()):
            UserFeaturedFriend.objects.create(user=self.pk, featured_user=user.pk)

    def create_or_plus_populate_friend(self, user_id):
        from users.model.list import UserPopulateFriend
        try:
            populate_friend = UserPopulateFriend.objects.get(user=self.pk, friend=user_id)
            populate_friend.count += 1
            populate_friend.save(update_fields=['count'])
        except:
            UserPopulateFriend.objects.create(user=self.pk, friend=user_id, count=1)

    def delete_populate_friend(self, user_id):
        from users.model.list import UserPopulateFriend
        try:
            populate_friend = UserPopulateFriend.objects.get(user=self.pk, friend=user_id)
            populate_friend.delete()
        except:
            pass

    def create_or_plus_populate_community(self, community_id):
        from users.model.list import UserPopulateCommunity
        try:
            populate_friend = UserPopulateCommunity.objects.get(user=self.pk, community=community_id)
            populate_friend.count += 1
            populate_friend.save(update_fields=['count'])
        except:
            UserPopulateCommunity.objects.create(user=self.pk, community=community_id, count=1)

    def delete_populate_community(self, community_id):
        from users.model.list import UserPopulateCommunity
        try:
            populate_friend = UserPopulateCommunity.objects.get(user=self.pk, community=community_id)
            populate_friend.delete()
        except:
            pass

    def remove_possible_friend(self, user_id):
        from users.model.list import UserFeaturedFriend
        if UserFeaturedFriend.objects.filter(user=self.pk, featured_user=user_id).exists():
            UserFeaturedFriend.objects.get(user=self.pk, featured_user=user_id).delete()

    def frend_user(self, user):
        self.frend_user_with_id(user.pk)
        user.plus_friends(1)
        self.plus_friends(1)
        self.minus_follows(1)
        self.create_or_plus_populate_friend(user.pk)
        user.create_or_plus_populate_friend(self.pk)
        try:
            for frend in user.get_6_friends():
                self.get_or_create_possible_friend(frend)
        except:
            pass

    def frend_user_with_id(self, user_id):
        from follows.models import Follow
        from frends.models import Connect
        from users.model.list import UserFeaturedFriend

        check_can_connect_with_user(user=self, user_id=user_id)
        if self.pk == user_id:
            raise ValidationError('Вы не можете добавить сами на себя',)
        frend = Connect.create_connection(user_id=self.pk, target_user_id=user_id)
        follow = Follow.objects.get(user=user_id, followed_user_id=self.pk)
        follow.delete()
        self.remove_possible_friend(user_id)
        self.add_news_subscriber(user_id)
        return frend

    def get_possible_friends(self):
        query = Q(id__in=self.get_possible_friends_ids())
        return User.objects.filter(query)

    def get_6_possible_friends(self):
        query = Q(id__in=self.get_6_possible_friends_ids())
        return User.objects.filter(query)

    def get_6_possible_friends_communities_ids(self):
        from communities.models import Community
        return [i['pk'] for i in Community.objects.filter(memberships__user__id__in=self.get_6_possible_friends()).values("pk")]

    def get_possible_friends_ids(self):
        from users.model.list import UserFeaturedFriend

        featured = UserFeaturedFriend.objects.filter(user=self.pk).values("featured_user")
        return [user['featured_user'] for user in featured]

    def get_possible_friends_count(self):
        from users.model.list import UserFeaturedFriend

        return UserFeaturedFriend.objects.filter(user=self.pk).values("featured_user").count()

    def get_6_possible_friends_ids(self):
        from users.model.list import UserFeaturedFriend

        featured = UserFeaturedFriend.objects.filter(user=self.pk).values("featured_user")
        return [user['featured_user'] for user in featured][:6]

    def unfollow_user(self, user):
        self.unfollow_user_with_id(user.pk)
        return user.minus_follows(1)

    def unfollow_user_with_id(self, user_id):
        from follows.models import Follow

        check_not_can_follow_user(user=self, user_id=user_id)
        follow = Follow.objects.get(user=self,followed_user_id=user_id).delete()
        self.delete_news_subscriber(user_id)

    def get_or_create_possible_friend(self, user):
        from users.model.list import UserFeaturedFriend

        if self.pk != user.pk and not UserFeaturedFriend.objects.filter(user=self.pk, featured_user=user.pk).exists() \
            and not self.is_connected_with_user_with_id(user_id=user.pk) and not self.is_blocked_with_user_with_id(user_id=user.pk) \
            and not (self.is_child() and not user.is_child_safety()):
            UserFeaturedFriend.objects.create(user=self.pk, featured_user=user.pk)

    def unfrend_user(self, user):
        self.unfrend_user_with_id(user.pk)
        user.minus_friends(1)
        self.minus_friends(1)
        self.plus_follows(1)
        return self.get_or_create_possible_friend(user)

    def unfrend_user_with_id(self, user_id):
        from follows.models import Follow

        check_is_following_user(user=self, user_id=user_id)
        follow = Follow.create_follow(user_id=user_id, followed_user_id=self.pk)
        follow.view = True
        follow.save(update_fields=["view"])
        self.delete_populate_friend(user_id)
        if self.is_closed_profile():
            self.delete_news_subscriber(user_id)
        connection = self.connections.get(target_connection__user_id=user_id)
        return connection.delete()

    def disconnect_from_user_with_id(self, user_id):
        check_is_connected(user=self, user_id=user_id)
        if self.is_following_user_with_id(user_id):
            self.unfollow_user_with_id(user_id)
        connection = self.connections.get(target_connection__user_id=user_id)
        connection.delete()

    def unblock_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        self.get_or_create_possible_friend(user)
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
        self.remove_possible_friend(user_id)
        self.delete_news_subscriber(user_id)
        self.delete_profile_subscriber(user_id)
        return user_to_block

    def search_followers_with_query(self, query):
        followers_query = Q(follows__followed_user_id=self.pk, is_deleted=False)
        names_query = Q(username__icontains=query)
        names_query.add(Q(profile__name__icontains=query), Q.OR)
        followers_query.add(names_query, Q.AND)
        return User.objects.filter(followers_query).distinct()

    def search_followings_with_query(self, query):
        followings_query = Q(followers__user_id=self.pk, is_deleted=False)
        names_query = Q(username__icontains=query)
        names_query.add(Q(profile__name__icontains=query), Q.OR)
        followings_query.add(names_query, Q.AND)
        return User.objects.filter(followings_query).distinct()

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
        return self.user_voter.filter(survey__pk=survey_pk).exists()
    def get_vote_of_survey(self, survey_pk):
        return self.user_voter.filter(survey__pk=survey_pk)[0]

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
        from music.models import UserTempSoundList
        return UserTempSoundList.objects.filter(user=self, tag=None, genre=None).exists()

    def is_user_temp_list(self, list):
        from music.models import UserTempSoundList
        return UserTempSoundList.objects.filter(user=self, tag=None, genre=None, list=list).exists()

    def is_tag_playlist(self, tag):
        from music.models import UserTempSoundList
        return UserTempSoundList.objects.filter(user=self, tag=tag, genre=None).exists()

    def is_genre_playlist(self, genre):
        from music.models import UserTempSoundList
        return UserTempSoundList.objects.get(user=self, tag=None, list=None, genre=genre).exists()

    def is_user_administrator(self):
        return try_except(self.user_staff.level == "A")
    def is_user_moderator(self):
        return try_except(self.user_staff.level == "M")
    def is_user_editor(self):
        return try_except(self.user_staff.level == "E")
    def is_user_advertiser(self):
        return try_except(self.user_staff.level == "R")
    def is_user_manager(self):
        try:
            return self.user_staff.level and self.user_staff.level != "R"
        except:
            return False

    def is_community_administrator(self):
        return try_except(self.user_community_staff.level == "A")
    def is_community_moderator(self):
        return try_except(self.user_community_staff.level == "M")
    def is_community_editor(self):
        return try_except(self.user_community_staff.level == "E")
    def is_community_advertiser(self):
        return try_except(self.user_community_staff.level == "R")
    def is_community_manager(self):
        try:
            return self.user_community_staff.level and self.user_community_staff.level != "R"
        except:
            return False

    def is_post_administrator(self):
        return try_except(self.post_user_staff.level == "A")
    def is_post_moderator(self):
        return try_except(self.post_user_staff.level == "M")
    def is_post_editor(self):
        return try_except(self.post_user_staff.level == "E")
    def is_post_manager(self):
        try:
            return self.post_user_staff.level
        except:
            return False

    def is_good_administrator(self):
        return try_except(self.good_user_staff.level == "A")
    def is_good_moderator(self):
        return try_except(self.good_user_staff.level == "M")
    def is_good_editor(self):
        return try_except(self.good_user_staff.level == "E")
    def is_good_manager(self):
        try:
            return self.good_user_staff.level
        except:
            return False

    def is_doc_administrator(self):
        return try_except(self.doc_user_staff.level == "A")
    def is_doc_moderator(self):
        return try_except(self.doc_user_staff.level == "M")
    def is_doc_editor(self):
        return try_except(self.doc_user_staff.level == "E")
    def is_doc_manager(self):
        try:
            return self.doc_user_staff.level
        except:
            return False


    def is_photo_administrator(self):
        return try_except(self.photo_user_staff.level == "A")
    def is_photo_moderator(self):
        return try_except(self.photo_user_staff.level == "M")
    def is_photo_editor(self):
        return try_except(self.photo_user_staff.level == "E")
    def is_photo_manager(self):
        try:
            return self.photo_user_staff.level
        except:
            return False

    def is_video_administrator(self):
        return try_except(self.video_user_staff.level == "A")
    def is_video_moderator(self):
        return try_except(self.video_user_staff.level == "M")
    def is_video_editor(self):
        return try_except(self.video_user_staff.level == "E")
    def is_video_manager(self):
        try:
            return self.video_user_staff.level
        except:
            return False

    def is_audio_administrator(self):
        return try_except(self.music_user_staff.level == "A")
    def is_audio_moderator(self):
        return try_except(self.music_user_staff.level == "M")
    def is_audio_editor(self):
        return try_except(self.music_user_staff.level == "E")
    def is_audio_manager(self):
        try:
            return self.music_user_staff.level
        except:
            return False

    def is_work_administrator(self):
        return try_except(self.can_work_staff_user.can_work_administrator)
    def is_work_moderator(self):
        return try_except(self.can_work_staff_user.can_work_moderator)
    def is_work_editor(self):
        return try_except(self.can_work_staff_user.can_work_editor)
    def is_work_advertiser(self):
        return try_except(self.can_work_staff_user.can_work_advertiser)
    def is_user_supermanager(self):
        return self.is_work_administrator() or self.is_work_moderator() or is_work_editor() or is_work_advertiser()

    def is_work_community_administrator(self):
        return try_except(self.can_work_staff_community.can_work_administrator)
    def is_work_community_moderator(self):
        return try_except(self.can_work_staff_community.can_work_moderator)
    def is_work_community_editor(self):
        return try_except(self.can_work_staff_community.can_work_editor)
    def is_work_community_advertiser(self):
        return try_except(self.can_work_staff_community.can_work_advertiser)
    def is_community_supermanager(self):
        return self.is_work_community_administrator() or self.is_work_community_moderator() or is_work_community_editor() or is_work_community_advertiser()

    def is_work_post_administrator(self):
        return try_except(self.can_work_staff_post_user.can_work_administrator)
    def is_work_post_moderator(self):
        return try_except(self.can_work_staff_post_user.can_work_moderator)
    def is_work_post_editor(self):
        return try_except(self.can_work_staff_post_user.can_work_editor)
    def is_work_supermanager(self):
        return self.is_work_post_administrator() or self.is_work_post_moderator() or is_work_post_editor()

    def is_work_good_administrator(self):
        return try_except(self.can_work_staff_good_user.can_work_administrator)
    def is_work_good_moderator(self):
        return try_except(self.can_work_staff_good_user.can_work_moderator)
    def is_work_good_editor(self):
        return try_except(self.can_work_staff_good_user.can_work_editor)
    def is_work_good_supermanager(self):
        return self.is_work_good_administrator() or self.is_work_good_moderator() or is_work_good_editor()

    def is_work_doc_administrator(self):
        return try_except(self.can_work_staff_doc_user.can_work_administrator)
    def is_work_doc_moderator(self):
        return try_except(self.can_work_staff_doc_user.can_work_moderator)
    def is_work_doc_editor(self):
        return try_except(self.can_work_staff_doc_user.can_work_editor)
    def is_work_doc_supermanager(self):
        return self.is_work_doc_administrator() or self.is_doc_good_moderator() or is_work_doc_editor()

    def is_work_photo_administrator(self):
        return try_except(self.can_work_staff_photo_user.can_work_administrator)
    def is_work_photo_moderator(self):
        return try_except(self.can_work_staff_photo_user.can_work_moderator)
    def is_work_photo_editor(self):
        return try_except(self.can_work_staff_photo_user.can_work_editor)
    def is_work_photo_supermanager(self):
        return self.is_work_photo_administrator() or self.is_work_photo_moderator() or is_work_photo_editor()

    def is_work_video_administrator(self):
        return try_except(self.can_work_staff_video_user.can_work_administrator)
    def is_work_video_moderator(self):
        return try_except(self.can_work_staff_video_user.can_work_moderator)
    def is_work_video_editor(self):
        return try_except(self.can_work_staff_video_user.can_work_editor)
    def is_work_video_supermanager(self):
        return self.is_work_video_administrator() or self.is_work_video_moderator() or is_work_video_editor()

    def is_work_music_administrator(self):
        return try_except(self.can_work_staff_music_user.can_work_administrator)
    def is_work_music_moderator(self):
        return try_except(self.can_work_staff_music_user.can_work_moderator)
    def is_work_music_editor(self):
        return try_except(self.can_work_staff_music_user.can_work_editor)
    def is_music_supermanager(self):
        return self.is_work_music_administrator() or self.is_work_music_moderator() or is_work_music_editor()

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
        self.profile.photos -= count
        return self.profile.save(update_fields=['photos'])
    def plus_goods(self, count):
        self.profile.goods += count
        return self.profile.save(update_fields=['goods'])
    def minus_goods(self, count):
        self.profile.goods -= count
        return self.profile.save(update_fields=['goods'])
    def plus_posts(self, count):
        self.profile.posts += count
        return self.profile.save(update_fields=['posts'])
    def minus_posts(self, count):
        self.profile.posts -= count
        return self.profile.save(update_fields=['posts'])
    def plus_videos(self, count):
        self.profile.videos += count
        return self.profile.save(update_fields=['videos'])
    def minus_videos(self, count):
        self.profile.videos -= count
        return self.profile.save(update_fields=['videos'])
    def plus_docs(self, count):
        self.profile.docs += count
        return self.profile.save(update_fields=['docs'])
    def minus_docs(self, count):
        self.profile.docs -= count
        return self.profile.save(update_fields=['docs'])
    def plus_tracks(self, count):
        self.profile.tracks += count
        return self.profile.save(update_fields=['tracks'])
    def minus_tracks(self, count):
        self.profile.tracks -= count
        return self.profile.save(update_fields=['tracks'])
    def plus_communities(self, count):
        self.profile.communities += count
        return self.profile.save(update_fields=['communities'])
    def minus_communities(self, count):
        self.profile.communities -= count
        return self.profile.save(update_fields=['communities'])
    def plus_articles(self, count):
        self.profile.articles += count
        return self.profile.save(update_fields=['articles'])
    def minus_articles(self, count):
        self.profile.articles -= count
        return self.profile.save(update_fields=['articles'])
    def plus_friends(self, count):
        self.profile.friends += count
        return self.profile.save(update_fields=['friends'])
    def minus_friends(self, count):
        self.profile.friends -= count
        return self.profile.save(update_fields=['friends'])
    def plus_follows(self, count):
        self.profile.follows += count
        return self.profile.save(update_fields=['follows'])
    def minus_follows(self, count):
        self.profile.follows -= count
        return self.profile.save(update_fields=['follows'])


    ''''' GET всякие  219-186 '''''
    def get_6_default_connection(self):
        my_frends = self.connections.values('target_user_id')
        connection_query = Q(id__in=[i['target_user_id'] for i in my_frends])
        connection_query.add(~Q(Q(blocked_by_users__blocker_id=self.id) | Q(user_blocks__blocked_user_id=self.id)), Q.AND)
        return User.objects.filter(connection_query)[0:6]

    def get_6_populate_friends_ids(self):
        from users.model.list import UserPopulateFriend
        frends_query = UserPopulateFriend.objects.filter(user=self.pk).values("friend")
        return [user['friend'] for user in frends_query][:6]

    def get_6_populate_friends(self):
        query = []
        for frend_id in self.get_6_populate_friends_ids():
            query.append(User.objects.get(pk=frend_id))
        return query

    def get_6_friends(self):
        try:
            return self.get_6_populate_friends()
        except:
            return self.get_6_default_connection()

    def get_6_default_communities(self):
        from communities.models import Community
        return Community.objects.filter(memberships__user=self)[0:6]

    def get_6_populate_communities(self):
        from users.model.list import UserPopulateCommunity
        from communities.models import Community

        communities_query = UserPopulateCommunity.objects.filter(user=self.pk).values("community")
        return Community.objects.filter(id__in=[i['community'] for i in communities_query][:6])

    def get_default_communities(self):
        from communities.models import Community
        return Community.objects.filter(memberships__user_id=self.pk)

    def get_populate_communities(self):
        from users.model.list import UserPopulateCommunity
        from communities.models import Community

        communities_query = UserPopulateCommunity.objects.filter(user=self.pk).values("community")
        return Community.objects.filter(id__in=[i['community'] for i in communities_query])

    def get_6_communities(self):
        try:
            return self.get_6_populate_communities()
        except:
            return self.get_6_default_communities()

    def get_communities(self):
        try:
            return self.get_populate_communities()
        except:
            return self.get_default_communities()

    def get_all_connection_ids(self):
        my_frends = self.connections.values('target_user_id')
        return [i['target_user_id'] for i in my_frends]

    def get_friend_and_friend_of_friend_ids(self):
        frends = self.get_all_connection()
        frends_ids = [u['id'] for u in frends.values('id')]
        query = []
        for frend in frends:
            i = frend.get_all_connection().values('id')
            query = query + [user['id'] for user in i]
        query = query + frends_ids
        set_query = list(set(query))
        try:
            set_query.remove(self.pk)
        except:
            pass
        return set_query


    def get_all_connection(self):
        connection_query = Q(id__in=self.get_all_connection_ids())
        return User.objects.filter(connection_query)

    def get_online_connection(self):
        frends, query = self.get_all_connection(), []
        for frend in frends:
            if frend.get_online():
                query += [frend,]
        return query

    def get_online_connection_count(self):
        frends, query = self.get_all_connection(), []
        for frend in frends:
            if frend.get_online():
                query += [frend,]
        return len(query)

    def get_pop_online_connection(self):
        frends, query = self.get_all_connection(), []
        for frend in frends:
            if frend.get_online() and len(query) < 6:
                query += [frend]
        return query

    def get_draft_posts(self):
        from posts.models import Post
        return Post.objects.filter(creator_id=self.id, type=Post.DRAFT, community__isnull=True)

    def get_draft_posts_of_community_with_pk(self, community_pk):
        from posts.models import Post
        return Post.objects.filter(creator_id=self.id, community_id=community_pk, type=Post.DRAFT)

    def get_6_populate_friends(self):
        query = []
        for frend_id in self.get_6_populate_friends_ids():
            query.append(User.objects.get(pk=frend_id))
        return query

    def get_post_lists(self):
        from posts.models import PostList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return PostList.objects.filter(query)

    def get_selected_post_list_pk(self):
        from users.model.list import UserPostListPosition
        list = UserPostListPosition.objects.filter(user=self.pk).first()
        return list.list

    def get_survey_lists(self):
        from survey.models import SurveyList
        query = Q(creator_id=self.id, community__isnull=True)
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

    def get_video_lists(self):
        from video.models import VideoList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return VideoList.objects.filter(query)

    def get_playlists(self):
        from music.models import SoundList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return SoundList.objects.filter(query)

    def get_good_lists(self):
        from goods.models import GoodList
        query = Q(creator_id=self.id, community__isnull=True)
        query.add(~Q(type__contains="_"), Q.AND)
        return GoodList.objects.filter(query)

    def get_good_list(self):
        from goods.models import GoodList
        return GoodList.objects.get(creator_id=self.pk, community__isnull=True, type="MAI")
    def get_playlist(self):
        from music.models import SoundList
        return SoundList.objects.get(creator_id=self.pk, community__isnull=True, type=SoundList.MAIN)
    def get_video_list(self):
        from video.models import VideoList
        return VideoList.objects.get(creator_id=self.pk, community__isnull=True, type=VideoList.MAIN)
    def get_photo_list(self):
        from gallery.models import PhotoList
        return PhotoList.objects.get(creator_id=self.pk, community__isnull=True, type=PhotoList.MAIN)
    def get_post_list(self):
        from posts.models import PostList
        return PostList.objects.get(creator_id=self.pk, community__isnull=True, type=PostList.MAIN)
    def get_doc_list(self):
        from docs.models import DocList
        return DocList.objects.get(creator_id=self.pk, community__isnull=True, type=DocList.MAIN)
    def get_fix_list(self):
        from posts.models import PostList
        return PostList.objects.get(creator_id=self.pk, community__isnull=True, type=PostList.FIXED)
    def get_survey_list(self):
        from survey.models import SurveyList
        return SurveyList.objects.get(creator_id=self.pk, community__isnull=True, type=SurveyList.MAIN)
    def get_playlists(self):
        from music.models import SoundList
        return SoundList.objects.filter(creator_id=self.id, community__isnull=True).exclude(type__contains="_")

    def is_photo_open(self, user_pk):
        from users.model.settings import UserPrivate

        private = UserPrivate.objects.get(user=self)
        if private.can_see_photo == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_photo == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_photo == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_photo == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_photo == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserPhotoCanSeeGalleryExcludes
            return not UserPhotoCanSeeGalleryExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_photo == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserPhotoCanSeeGalleryIncludes
            return UserPhotoCanSeeGalleryIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_post_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_see_post == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_post == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_post == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_post == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_post == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserPostCanSeeGalleryExcludes
            return not UserPostCanSeeGalleryExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_post == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserPostCanSeeGalleryIncludes
            return UserPostCanSeeGalleryIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_video_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_see_video == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_video == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_video == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_video == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_video == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserVideoCanSeeVideoExcludes
            return not UserVideoCanSeeVideoExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_video == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserVideoCanSeeVideoIncludes
            return UserVideoCanSeeVideoIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_music_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_see_music == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_music == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_music == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_music == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_music == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserMusicCanSeeMusicExcludes
            return not UserMusicCanSeeMusicExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_music == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserMusicCanSeeMusicIncludes
            return UserMusicCanSeeMusicIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_good_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_see_good == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_good == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_good == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_good == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_good == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserGoodCanSeeMarketExcludes
            return not UserGoodCanSeeMarketExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_good == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserGoodCanSeeMarketIncludes
            return UserGoodCanSeeMarketIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_community_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_see_community == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_community == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_community == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_community == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_community == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserCommunityCanSeeExcludes
            return not UserCommunityCanSeeExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_community == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserCommunityCanSeeIncludes
            return UserCommunityCanSeeIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_friend_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_see_friend == UserPrivate.ALL_CAN:
            return True
        elif private.can_see_friend == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_see_friend == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_see_friend == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_see_friend == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserFriendCanSeeExcludes
            return not UserFriendCanSeeExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_see_friend == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserFriendCanSeeIncludes
            return UserFriendCanSeeIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_message_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_receive_message == UserPrivate.ALL_CAN:
            return True
        elif private.can_receive_message == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_receive_message == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_receive_message == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_receive_message == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserMessageCanSeeExcludes
            return not UserMessageCanSeeExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_receive_message == UserPrivate.SOME_FRIENDS:
            from users.model.list import UserMessageCanSeeIncludes
            return UserMessageCanSeeIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def is_doc_open(self, user_pk):
        from users.model.settings import UserPrivate
        private = UserPrivate.objects.get(user=self)

        if private.can_receive_doc == UserPrivate.ALL_CAN:
            return True
        elif private.can_receive_doc == UserPrivate.FRIENDS and user_pk in self.get_all_connection_ids():
            return True
        elif private.can_receive_doc == UserPrivate.EACH_OTHER and user_pk in self.get_friend_and_friend_of_friend_ids():
            return True
        elif private.can_receive_doc == UserPrivate.YOU and user_pk == self.pk:
            return True
        elif private.can_receive_doc == UserPrivate.FRIENDS_BUT:
            from users.model.list import UserDocCanSeeExcludes
            return not UserDocCanSeeExcludes.objects.filter(owner=self.pk, user=user_pk).exists()
        elif private.can_receive_doc== UserPrivate.SOME_FRIENDS:
            from users.model.list import UserDocCanSeeIncludes
            return UserDocCanSeeIncludes.objects.filter(owner=self.pk, user=user_pk).exists()
        else:
            return False

    def get_6_photos(self):
        from gallery.models import Photo
        from users.model.settings import UserPrivate

        private = UserPrivate.objects.get(user=self)

    def get_music_count(self):
        return self.profile.tracks

    def get_last_music(self):
        return self.get_playlist().get_items()[:6]

    def get_video_count(self):
        return self.profile.videos

    def get_last_video(self):
        return self.get_video_list().get_items()[:2]

    def my_playlist_too(self):
        from music.models import SoundList, UserTempSoundList, SoundTags, SoundGenres

        if UserTempSoundList.objects.filter(user_id=self.pk).exists():
            temp_list = UserTempSoundList.objects.get(user_id=self.pk)
        else:
            return self.get_playlist().get_items()
        try:
            return SoundList.objects.get(pk=temp_list.list.pk).get_items()
        except:
            pass
        try:
            return SoundTags.objects.get(pk=temp_list.tag.pk).get_items()
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

    def get_doc_lists(self):
        from docs.models import DocList
        return DocList.objects.filter(creator_id=self.id, community__isnull=True).exclude(type__contains="_")

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
        return community_to_join

    def add_news_subscriber(self, user_id):
        from notify.models import UserNewsNotify
        if not UserNewsNotify.objects.filter(user=self.pk, target=user_id).exists():
            UserNewsNotify.objects.create(user=self.pk, target=user_id)
    def delete_news_subscriber(self, user_id):
        from notify.models import UserNewsNotify
        if UserNewsNotify.objects.filter(user=self.pk, target=user_id).exists():
            notify = UserNewsNotify.objects.get(user=self.pk, target=user_id)
            notify.delete()

    def add_notify_subscriber(self, user_id):
        from notify.models import UserProfileNotify
        if not UserProfileNotify.objects.filter(user=self.pk, target=user_id).exists():
            UserProfileNotify.objects.create(user=self.pk, target=user_id)
    def delete_notify_subscriber(self, user_id):
        from notify.models import UserProfileNotify
        if UserProfileNotify.objects.filter(user=self.pk, target=user_id).exists():
            notify = UserProfileNotify.objects.get(user=self.pk, target=user_id)
            notify.delete()

    def get_user_news_notify_ids(self):
        from notify.models import UserNewsNotify
        return [i['target'] for i in UserNewsNotify.objects.filter(user=self.pk).values('target')]
    def get_community_news_notify_ids(self):
        from notify.models import CommunityNewsNotify
        return [i['community'] for i in CommunityNewsNotify.objects.filter(user=self.pk).values('community')]

    def get_user_profile_notify_ids(self):
        from notify.models import UserProfileNotify
        return [i['target'] for i in UserProfileNotify.objects.filter(user=self.pk).values('target')]
    def get_community_profile_notify_ids(self):
        from notify.models import CommunityProfileNotify
        return [i['community'] for i in CommunityProfileNotify.objects.filter(user=self.pk).values('community')]


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

    def get_longest_user_penalties(self):
        return self.user_penalties.filter(user=self)[0].expiration
    def get_moderated_description(self):
        return self.moderated_user.filter(user=self)[0].description

    ''''' начало сообщения '''''

    def get_private_chats(self):
        from chat.models import Chat
        return Chat.objects.filter(chat_relation__user_id=self.pk, type=Chat.PRIVATE)

    def get_all_chats(self):
        from chat.models import Chat
        return Chat.objects.filter(chat_relation__user_id=self.pk).exclude(type__contains="_")

    def get_chats_and_connections(self):
        from itertools import chain
        return list(chain(self.get_all_chats(), self.get_all_connection()))

    def is_administrator_of_chat(self, chat_pk):
        return self.chat_users.filter(chat__pk=chat_pk, is_administrator=True).exists()
    def is_member_of_chat(self, chat_pk):
        return self.chat_users.filter(chat__pk=chat_pk).exists()

    def get_unread_chats(self):
        chats, count = self.get_all_chats(), 0
        for chat in chats:
            if chat.chat_message.filter(unread=True, type__contains="_").exclude(creator_id=self.pk).exists():
                count += 1
        if count > 0:
            return count
        else:
            return ''

    def get_user_notify(self):
        from notify.models import Notify

        query = Q(creator_id__in=self.get_user_profile_notify_ids())| \
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
        from notify.models import UserProfileNotify
        recipients = UserProfileNotify.objects.filter(user=self.pk).values("target")
        return [i['target'] for i in recipients]
