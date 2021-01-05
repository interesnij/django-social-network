import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from common.utils import try_except
from common.check.user import *
from users.helpers import upload_to_user_directory


class User(AbstractUser):
    DELETED, BLOCKED, PHONE_NO_VERIFIED, CHILD, STANDART, VERIFIED_SEND, VERIFIED, IDENTIFIED_SEND, IDENTIFIED, MANAGER, SUPERMANAGER = 'DE', 'BL', 'PV', 'CH', 'ST', 'VS', 'VE', 'IS', 'ID', 'MA', 'SM'
    PERM = (
        (DELETED, 'Удален'),
        (BLOCKED, 'Заблокирован'),
        (CHILD, 'Ребенок'),
        (PHONE_NO_VERIFIED, 'Телефон не подтвержден'),
        (STANDART, 'Обычные права'),
        (VERIFIED_SEND, 'Запрос на проверку'),
        (VERIFIED, 'Проверенный'),
        (IDENTIFIED_SEND, 'Запрос на идентификацию'),
        (IDENTIFIED, 'Идентифицированный'),
        (MANAGER, 'Менеджер'),
        (SUPERMANAGER, 'Суперменеджер'),
    )
    MALE, FEMALE, DESCTOP, PHONE = 'Man', 'Fem', 'De', 'Ph'
    GENDER = ((MALE, 'Мужской'),(FEMALE, 'Женский'),)
    DEVICE = ((DESCTOP, 'Комп'),(PHONE, 'Телефон'),)

    id = models.BigAutoField(primary_key=True)
    last_activity = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, unique=True, verbose_name='Телефон')
    perm = models.CharField(max_length=5, choices=PERM, default=PHONE_NO_VERIFIED, verbose_name="Уровень доступа")
    gender = models.CharField(max_length=5, choices=GENDER, blank=True, verbose_name="Пол")
    device = models.CharField(max_length=5, choices=DEVICE, blank=True, verbose_name="Оборудование")
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    have_link = models.CharField(max_length=17, blank=True, verbose_name='Ссылка')
    sity = models.CharField(max_length=settings.PROFILE_LOCATION_MAX_LENGTH, blank=True, verbose_name="Местоположение")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")

    #post = models.ManyToManyField("posts.Post", blank=True, related_name='post_user')

    #USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()

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

    def calculate_age(birthday):
        from datetime import date

        today = date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def is_women(self):
        return try_except(self.perm == User.FEMALE)
    def is_men(self):
        return try_except(self.perm == User.MALE)
    def is_no_gender(self):
        return try_except(self.perm == User.UNCNOUN)

    def is_deleted(self):
        return try_except(self.perm == User.DELETED)
    def is_manager(self):
        return try_except(self.perm == User.MANAGER)
    def is_supermanager(self):
        return try_except(self.perm == User.SUPERMANAGER)
    def is_verified_send(self):
        return try_except(self.perm == User.VERIFIED_SEND)
    def is_verified(self):
        return try_except(self.perm == User.VERIFIED)
    def is_identified_send(self):
        return try_except(self.perm == User.IDENTIFIED_SEND)
    def is_identified(self):
        return try_except(self.perm == User.IDENTIFIED)
    def is_child(self):
        return try_except(self.perm == User.CHILD)
    def is_no_phone_verified(self):
        return try_except(self.perm == User.PHONE_NO_VERIFIED)
    def is_child_safety(self):
        if self.perm == User.MANAGER or self.perm == User.SUPERMANAGER or self.perm == User.VERIFIED:
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

    def notification_follow(self, user):
        from notify.model.user import UserNotify, notification_handler

        notification_handler(creator=self, recipient=user, verb=UserNotify.CONNECTION_REQUEST)
    def notification_connect(self, user):
        from notify.model.user import UserNotify, notification_handler

        notification_handler(creator=self, recipient=user, verb=UserNotify.CONNECTION_CONFIRMED)

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

    def get_photos_count(self):
        return self.photo_creator.values("pk").count()

    def get_online(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=3)
        if now < onl:
            return True
        else:
            return False
    def get_online_display(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=3)
        if self.device == User.DESCTOP:
            device = '&nbsp;<svg style="width: 17px;" class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 18c1.1 0 1.99-.9 1.99-2L22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zM4 6h16v10H4V6z"/></svg>'
        else:
            device = '&nbsp;<svg style="width: 17px;" class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>'
        if now < onl:
            return '<i>Онлайн</i>' + device
        else:
            if self.is_women():
                return '<i>Была' + self.get_last_activity() + '</i>' + device
            else:
                return '<i>Был' + self.get_last_activity() + '</i>' + device


    def get_request_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_blocked_users(self):
        blocked_users_query = Q(blocked_by_users__blocker_id=self.pk)
        return User.objects.filter(blocked_users_query).distinct()

    def get_staffed_communities(self):
        from communities.models import Community

        query = Q(Q(memberships__user=self, memberships__is_administrator=True) | Q(memberships__user=self, memberships__is_editor=True))
        return Community.objects.filter(query)

        '''''проги для подписчиков  60-109'''''

    def follow_user(self, user):
        return self.follow_user_with_id(user.pk)

    def follow_user_with_id(self, user_id):
        from follows.models import Follow

        check_can_follow_user(user_id=user_id, user=self)
        if self.pk == user_id:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        return Follow.create_follow(user_id=self.pk, followed_user_id=user_id)

    def community_follow_user(self, community_pk):
        return self.follow_community(community_pk)

    def follow_community(self, community_pk):
        from follows.models import CommunityFollow

        check_can_join_community(user=self, community_pk=community_pk)
        return CommunityFollow.create_follow(user_id=self.pk, community_pk=community_pk)

    def community_unfollow_user(self, community_pk):
        return self.unfollow_community(community_pk)

    def unfollow_community(self, community_pk):
        from follows.models import CommunityFollow

        check_can_join_community(user=self, community_pk=community_pk)
        follow = CommunityFollow.objects.get(user=self,community__pk=community_pk)
        follow.delete()

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
        try:
            for frend in user.get_6_friends():
                self.get_or_create_possible_friend(frend)
        except:
            pass

    def get_possible_friends(self):
        query = Q(id__in=self.get_possible_friends_ids())
        return User.objects.filter(query)

    def get_6_possible_friends(self):
        query = Q(id__in=self.get_6_possible_friends_ids())
        return User.objects.filter(query)

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
        self.create_or_plus_populate_friend(user_id)
        return frend

    def unfollow_user(self, user):
        return self.unfollow_user_with_id(user.pk)

    def unfollow_user_with_id(self, user_id):
        from follows.models import Follow

        check_not_can_follow_user(user=self, user_id=user_id)
        follow = Follow.objects.get(user=self,followed_user_id=user_id)
        follow.delete()

    def get_or_create_possible_friend(self, user):
        from users.model.list import UserFeaturedFriend

        if self.pk != user.pk and not UserFeaturedFriend.objects.filter(user=self.pk, featured_user=user.pk).exists() \
            and not self.is_connected_with_user_with_id(user_id=user.pk) and not self.is_blocked_with_user_with_id(user_id=user.pk) \
            and not (self.is_child() and not user.is_child_safety()):
            UserFeaturedFriend.objects.create(user=self.pk, featured_user=user.pk)

    def unfrend_user(self, user):
        self.unfrend_user_with_id(user.pk)
        return self.get_or_create_possible_friend(user)

    def unfrend_user_with_id(self, user_id):
        from follows.models import Follow

        check_is_following_user(user=self, user_id=user_id)
        follow = Follow.create_follow(user_id=user_id, followed_user_id=self.pk)
        follow.view = True
        follow.save(update_fields=["view"])
        self.delete_populate_friend(user_id)
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

    def is_connected_with_user_with_username(self, username):
        return self.connections.filter(target_connection__user__username=username).exists()

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

    def is_closed_profile(self):
        from users.model.settings import UserPrivate
        try:
            user_private = UserPrivate.objects.get(user=self)
            return user_private.is_private
        except:
            user_private = UserPrivate.objects.create(user=self)
            return False

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


    def is_public_album_exists(self):
        return self.photo_album_creator.filter(creator_id=self.pk, community__isnull=True, is_public=True).exists()
    def is_album_exists(self):
        return self.photo_album_creator.filter(creator_id=self.pk, community__isnull=True).exists()

    def is_photo_exists(self):
        return self.photo_creator.filter(creator_id=self.pk, community__isnull=True).exists()

    def is_suspended(self):
        return self.user_penalties.filter(type="S", expiration__gt=timezone.now()).exists()
    def is_blocked(self):
        return self.user_penalties.filter(type="B").exists()
    def is_have_warning_banner(self):
        return self.user_penalties.filter(type="BA").exists()

    def is_track_exists(self, track_id):
        from music.models import SoundList, SoundcloudParsing

        return SoundList.objects.values("creator", "players").filter(creator=self, players__id=track_id).exists()

    def is_user_playlist(self):
        from music.models import UserTempSoundList
        try:
            UserTempSoundList.objects.get(user=self, tag=None, genre=None)
            return True
        except:
            return False

    def is_user_temp_list(self, list):
        from music.models import UserTempSoundList
        try:
            UserTempSoundList.objects.get(user=self, tag=None, genre=None, list=list)
            return True
        except:
            return False

    def is_tag_playlist(self, tag):
        from music.models import UserTempSoundList

        try:
            UserTempSoundList.objects.get(user=self, tag=tag, genre=None)
            return True
        except:
            return False

    def is_genre_playlist(self, genre):
        from music.models import UserTempSoundList

        try:
            UserTempSoundList.objects.get(user=self, tag=None, list=None, genre=genre)
            return True
        except:
            return False

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
            return try_except(self.user_staff.level and self.user_staff.level != "R")
        except:
            return None

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
            return try_except(self.user_community_staff.level and self.user_community_staff.level != "R")
        except:
            return None

    def is_post_administrator(self):
        return try_except(self.post_user_staff.level == "A")
    def is_post_moderator(self):
        return try_except(self.post_user_staff.level == "M")
    def is_post_editor(self):
        return try_except(self.post_user_staff.level == "E")
    def is_post_manager(self):
        try:
            return try_except(self.post_user_staff.level)
        except:
            return None

    def is_good_administrator(self):
        return try_except(self.good_user_staff.level == "A")
    def is_good_moderator(self):
        return try_except(self.good_user_staff.level == "M")
    def is_good_editor(self):
        return try_except(self.good_user_staff.level == "E")
    def is_good_manager(self):
        try:
            return try_except(self.good_user_staff.level)
        except:
            return None

    def is_photo_administrator(self):
        return try_except(self.photo_user_staff.level == "A")
    def is_photo_moderator(self):
        return try_except(self.photo_user_staff.level == "M")
    def is_photo_editor(self):
        return try_except(self.photo_user_staff.level == "E")
    def is_photo_manager(self):
        try:
            return try_except(self.photo_user_staff.level)
        except:
            return None

    def is_video_administrator(self):
        return try_except(self.video_user_staff.level == "A")
    def is_video_moderator(self):
        return try_except(self.video_user_staff.level == "M")
    def is_video_editor(self):
        return try_except(self.video_user_staff.level == "E")
    def is_video_manager(self):
        try:
            return try_except(self.video_user_staff.level)
        except:
            return None

    def is_audio_administrator(self):
        return try_except(self.music_user_staff.level == "A")
    def is_audio_moderator(self):
        return try_except(self.music_user_staff.level == "M")
    def is_audio_editor(self):
        return try_except(self.music_user_staff.level == "E")
    def is_audio_manager(self):
        try:
            return try_except(self.music_user_staff.level)
        except:
            return None

    def is_work_administrator(self):
        return try_except(self.can_work_staff_user.can_work_administrator)
    def is_work_moderator(self):
        return try_except(self.can_work_staff_user.can_work_moderator)
    def is_work_editor(self):
        return try_except(self.can_work_staff_user.can_work_editor)
    def is_work_advertiser(self):
        return try_except(self.can_work_staff_user.can_work_advertiser)
    def is_user_supermanager(self):
        if self.is_work_administrator() or self.is_work_moderator() or is_work_editor() or is_work_advertiser():
            return True
        else:
            return False

    def is_work_community_administrator(self):
        return try_except(self.can_work_staff_community.can_work_administrator)
    def is_work_community_moderator(self):
        return try_except(self.can_work_staff_community.can_work_moderator)
    def is_work_community_editor(self):
        return try_except(self.can_work_staff_community.can_work_editor)
    def is_work_community_advertiser(self):
        return try_except(self.can_work_staff_community.can_work_advertiser)
    def is_community_supermanager(self):
        if self.is_work_community_administrator() or self.is_work_community_moderator() or is_work_community_editor() or is_work_community_advertiser():
            return True
        else:
            return False

    def is_work_post_administrator(self):
        return try_except(self.can_work_staff_post_user.can_work_administrator)
    def is_work_post_moderator(self):
        return try_except(self.can_work_staff_post_user.can_work_moderator)
    def is_work_post_editor(self):
        return try_except(self.can_work_staff_post_user.can_work_editor)
    def is_work_supermanager(self):
        if self.is_work_post_administrator() or self.is_work_post_moderator() or is_work_post_editor():
            return True
        else:
            return False

    def is_work_good_administrator(self):
        return try_except(self.can_work_staff_good_user.can_work_administrator)
    def is_work_good_moderator(self):
        return try_except(self.can_work_staff_good_user.can_work_moderator)
    def is_work_good_editor(self):
        return try_except(self.can_work_staff_good_user.can_work_editor)
    def is_work_good_supermanager(self):
        if self.is_work_good_administrator() or self.is_work_good_moderator() or is_work_good_editor():
            return True
        else:
            return False

    def is_work_photo_administrator(self):
        return try_except(self.can_work_staff_photo_user.can_work_administrator)
    def is_work_photo_moderator(self):
        return try_except(self.can_work_staff_photo_user.can_work_moderator)
    def is_work_photo_editor(self):
        return try_except(self.can_work_staff_photo_user.can_work_editor)
    def is_work_photo_supermanager(self):
        if self.is_work_photo_administrator() or self.is_work_photo_moderator() or is_work_photo_editor():
            return True
        else:
            return False

    def is_work_video_administrator(self):
        return try_except(self.can_work_staff_video_user.can_work_administrator)
    def is_work_video_moderator(self):
        return try_except(self.can_work_staff_video_user.can_work_moderator)
    def is_work_video_editor(self):
        return try_except(self.can_work_staff_video_user.can_work_editor)
    def is_work_video_supermanager(self):
        if self.is_work_video_administrator() or self.is_work_video_moderator() or is_work_video_editor():
            return True
        else:
            return False

    def is_work_music_administrator(self):
        return try_except(self.can_work_staff_music_user.can_work_administrator)
    def is_work_music_moderator(self):
        return try_except(self.can_work_staff_music_user.can_work_moderator)
    def is_work_music_editor(self):
        return try_except(self.can_work_staff_music_user.can_work_editor)
    def is_music_supermanager(self):
        if self.is_work_music_administrator() or self.is_work_music_moderator() or is_work_music_editor():
            return True
        else:
            return False

    ''''' количества всякие  196-216 '''''

    def is_no_view_followers(self):
        return self.followers.filter(view=False).exists()

    def is_have_followers(self):
        return self.followers.values('pk').exists()
    def is_have_followings(self):
        return self.follows.values('pk').exists()
    def is_have_blacklist(self):
        return self.user_blocks.values('pk').exists()
    def is_have_friends(self):
        return self.connections.values('pk').exists()

    def count_no_view_followers(self):
        return self.followers.filter(view=False).values('pk').count()

    def count_following(self):
        return self.follows.values('pk').count()

    def count_followers(self):
        return self.followers.values('pk').count()

    def count_blacklist(self):
        return self.user_blocks.values('pk').count()

    def count_connections(self):
        return self.connections.values('pk').count()

    def count_community(self):
        return self.communities_memberships.values('pk').count()

    def count_albums(self):
        return self.photo_album_creator.filter(community__isnull=True, is_deleted=False).exclude(type="MA").values('pk').count()

    def count_goods(self):
        return self.good_creator.values('pk').count()

    def count_docs(self):
        return self.doc_creator.values('pk').count()

    def count_public_posts(self):
        return self.post_creator.filter(status="P").values('pk').count()
    def count_public_articles(self):
        return self.article_creator.filter(status="P").values('pk').count()


    ''''' GET всякие  219-186 '''''
    def get_6_default_connection(self):
        my_frends = self.connections.values('target_user_id')
        connection_query = Q(id__in=[target_user['target_user_id'] for target_user in my_frends])
        connection_query.add(~Q(Q(blocked_by_users__blocker_id=self.id) | Q(user_blocks__blocked_user_id=self.id)), Q.AND)
        return User.objects.filter(connection_query)[0:6]

    def get_6_populate_friends_ids(self):
        from users.model.list import UserPopulateFriend

        frends_query = UserPopulateFriend.objects.filter(user=self.pk).values("friend")
        return [user['friend'] for user in frends_query][:6]

    def is_have_friends(self):
        from frends.models import Connect

        return Connect.objects.filter(user_id=self.pk).exists()

    def get_6_populate_friends(self):
        query = []
        for frend_id in self.get_6_populate_friends_ids():
            user = User.objects.get(pk=frend_id)
            query = query + [user]
        return query

    def get_6_populate_object(self):
        from users.model.list import UserPopulateFriend

        frends_query = UserPopulateFriend.objects.filter(user=self.pk)
        return frends_query

    def get_6_friends(self):
        try:
            return self.get_6_populate_friends()
        except:
            return self.get_6_default_connection()

    def is_have_communities(self):
        from communities.models import Community

        return Community.objects.filter(memberships__user_id=self.pk).exists()

    def get_6_default_communities(self):
        from communities.models import Community

        query = Q(memberships__user=self)
        return Community.objects.filter(query)[0:6]

    def get_6_populate_communities(self):
        from users.model.list import UserPopulateCommunity
        from communities.models import Community

        communities_query, query = UserPopulateCommunity.objects.filter(user=self.pk).values("community"), []
        for community_id in [community['community'] for community in communities_query][:6]:
            community = Community.objects.get(pk=community_id)
            query = query + [community]
        return query

    def get_default_communities(self):
        from communities.models import Community

        query = Q(memberships__user=self)
        return Community.objects.filter(memberships__user_id=self.pk)

    def get_populate_communities(self):
        from users.model.list import UserPopulateCommunity
        from communities.models import Community

        communities_query = UserPopulateCommunity.objects.filter(user=self.pk).values("community")
        query = []
        for community_id in [community['community'] for community in communities_query]:
            community = Community.objects.get(pk=community_id)
            query = query + [community]
        return query

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
        return [target_user['target_user_id'] for target_user in my_frends]

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
        connection_query.add(~Q(Q(blocked_by_users__blocker_id=self.id) | Q(user_blocks__blocked_user_id=self.id)), Q.AND)
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

    def is_have_fixed_posts(self):
        from posts.models import PostList
        try:
            list = PostList.objects.get(creator_id=self.pk, community__isnull=True, type=PostList.FIX)
            if list.is_not_empty():
                return True
            else:
                return False
        except:
            pass
    def get_or_create_fix_list(self):
        from posts.models import PostList
        try:
            return PostList.objects.get(creator_id=self.pk, community__isnull=True, type=PostList.FIX)
        except:
            return PostList.objects.create(creator_id=self.pk, community__isnull=True, type=PostList.FIX, name="Закрепленный список")

    def get_draft_posts(self):
        from posts.models import Post

        posts_query = Q(creator_id=self.id, is_deleted=False, status=Post.STATUS_DRAFT, community__isnull=True)
        return Post.objects.filter(posts_query)

    def get_draft_posts_of_community_with_pk(self, community_pk):
        from posts.models import Post

        posts_query = Q(creator_id=self.id, community_id=community_pk, is_deleted=False, status=Post.STATUS_DRAFT)
        return Post.objects.filter(posts_query)

    def get_post_lists(self):
        from posts.models import PostList

        lists_query = Q(creator_id=self.id, community__isnull=True, is_deleted=False)
        lists_query.add(~Q(Q(type=PostList.DELETED)|Q(type=PostList.PRIVATE)|Q(type=PostList.FIX)), Q.AND)
        return PostList.objects.filter(lists_query).order_by("order")

    def get_post_categories(self):
        from posts.models import PostCategory
        return PostCategory.objects.only("pk")

    def get_my_all_post_lists(self):
        from posts.models import PostList
        lists_query = Q(creator_id=self.id, community__isnull=True, is_deleted=False)
        lists_query.add(~Q(Q(type=PostList.DELETED)|Q(type=PostList.FIX)), Q.AND)
        return PostList.objects.filter(lists_query)

    def get_articles(self):
        from article.models import Article

        articles_query = Q(creator_id=self.id, is_deleted=False)
        return Article.objects.filter(articles_query)

    def get_surveys(self):
        from survey.models import Survey

        query = Q(creator_id=self.id, is_deleted=False)
        return Survey.objects.filter(query)

    def get_all_albums(self):
        from gallery.models import Album

        albums_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community__isnull=True)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query).order_by("order")

    def get_albums(self):
        from gallery.models import Album

        albums_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community__isnull=True)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query).order_by("order")

    def get_my_albums(self):
        from gallery.models import Album

        albums_query = Q(creator_id=self.id, is_deleted=False, community__isnull=True)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query)

    def get_my_al_albums(self):
        from gallery.models import Album

        albums_query = Q(creator_id=self.id, is_deleted=False, community__isnull=True, type=Album.ALBUM)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query)

    def get_video_albums(self):
        from video.models import VideoAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community__isnull=True)
        return VideoAlbum.objects.filter(albums_query)

    def user_photo_album_exists(self):
        return self.photo_album_creator.filter(creator_id=self.id, community__isnull=True, is_deleted=False, type="AL").exists()
    def user_video_album_exists(self):
        return self.video_user_creator.filter(creator_id=self.id, community__isnull=True, is_deleted=False, type="AL").exists()
    def is_video_album_exists(self):
        return self.video_user_creator.filter(creator_id=self.id, community__isnull=True, is_public=True, is_deleted=False).exists()
    def is_music_playlist_exists(self):
        return self.user_playlist.filter(creator_id=self.id, community__isnull=True, type="LI", is_deleted=False).exists()
    def is_good_album_exists(self):
        return self.good_album_creator.filter(creator_id=self.id, community__isnull=True, type="AL", is_deleted=False).exists()
    def post_list_exists(self):
        return self.user_postlist.filter(creator_id=self.id, community__isnull=True, type="AL").exists()
    def my_post_list_exists(self):
        return self.user_postlist.filter(creator_id=self.id, community__isnull=True).exclude(type="MA").exists()

    def get_my_video_albums(self):
        from video.models import VideoAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, community__isnull=True, type="AL")
        return VideoAlbum.objects.filter(albums_query).order_by("order")

    def get_all_video_albums(self):
        from video.models import VideoAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, community__isnull=True)
        return VideoAlbum.objects.filter(albums_query).order_by("order")

    def get_audio_playlists(self):
        from music.models import SoundList

        playlists_query = Q(creator_id=self.id, community__isnull=True, type=SoundList.LIST, is_deleted=False)
        return SoundList.objects.filter(playlists_query).order_by("order")

    def get_all_audio_playlists(self):
        from music.models import SoundList

        playlists_query = Q(creator_id=self.id, community__isnull=True, is_deleted=False)
        return SoundList.objects.filter(playlists_query).order_by("order")

    def get_good_albums(self):
        from goods.models import GoodAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, community__isnull=True, type=GoodAlbum.ALBUM)
        return GoodAlbum.objects.filter(albums_query).order_by("order")

    def get_all_good_albums(self):
        from goods.models import GoodAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, community__isnull=True)
        return GoodAlbum.objects.filter(albums_query).order_by("order")

    def get_or_create_good_album(self):
        from goods.models import GoodAlbum
        try:
            return GoodAlbum.objects.get(creator_id=self.pk, community__isnull=True, type=GoodAlbum.MAIN)
        except:
            return GoodAlbum.objects.create(creator_id=self.pk, community__isnull=True, type=GoodAlbum.MAIN, title="Основной альбом")
    def get_or_create_playlist(self):
        from music.models import SoundList
        try:
            return SoundList.objects.get(creator_id=self.pk, community__isnull=True, type=SoundList.MAIN)
        except:
            return SoundList.objects.create(creator_id=self.pk, community__isnull=True, type=SoundList.MAIN, name="Основной плейлист")
    def get_or_create_video_album(self):
        from video.models import VideoAlbum
        try:
            return VideoAlbum.objects.get(creator_id=self.pk, community__isnull=True, type=VideoAlbum.MAIN)
        except:
            return VideoAlbum.objects.create(creator_id=self.pk, community__isnull=True, type=VideoAlbum.MAIN, title="Основной альбом")
    def get_or_create_photo_album(self):
        from gallery.models import Album
        try:
            return Album.objects.get(creator_id=self.pk, community__isnull=True, type=Album.MAIN)
        except:
            return Album.objects.create(creator_id=self.pk, community__isnull=True, type=Album.MAIN, title="Основной альбом")
    def get_or_create_doc_list(self):
        from docs.models import DocList
        try:
            return DocList.objects.get(creator_id=self.pk, community__isnull=True, type=DocList.MAIN)
        except:
            return DocList.objects.create(creator_id=self.pk, community__isnull=True, type=DocList.MAIN, title="Основной список")

    def get_music(self):
        from music.models import SoundList, SoundcloudParsing

        list = SoundList.objects.get(creator_id=self.id, community__isnull=True, type=SoundList.MAIN)
        return list.players.filter(is_deleted=False)

    def is_have_music(self):
        for list in self.get_playlists():
            if list.is_not_empty():
                return True
        return False

    def get_playlists(self):
        from music.models import SoundList

        return SoundList.objects.filter(creator_id=self.id, is_deleted=False, community__isnull=True)

    def get_music_count(self):
        count = 0
        for list in self.get_playlists():
            count += list.count_tracks()
        return count

    def get_last_music(self):
        lists = []
        for i in self.get_music():
            if len(lists) < 6:
                lists += [i]
        return lists

    def get_video_count(self):
        from video.models import Video, VideoAlbum

        list = VideoAlbum.objects.get(creator_id=self.id, community__isnull=True, type=VideoAlbum.MAIN)
        video_query = Q(album=list, is_deleted=False)
        return Video.objects.filter(video_query).values("pk").count()

    def get_last_video(self):
        from video.models import Video, VideoAlbum

        list = VideoAlbum.objects.get(creator_id=self.id, community__isnull=True, type=VideoAlbum.MAIN)
        video_query = Q(album=list, is_deleted=False, is_public=True)
        return Video.objects.filter(video_query).order_by("-created")[0:2]

    def my_playlist_too(self):
        from music.models import SoundList, UserTempSoundList, SoundTags, SoundGenres

        temp_list = UserTempSoundList.objects.get(user=self)
        try:
            list = SoundList.objects.get(pk=temp_list.list.pk)
        except:
            list = None
        try:
            tag_music = SoundTags.objects.get(pk=temp_list.tag.pk)
        except:
            tag_music = None
        try:
            genre_music = SoundGenres.objects.get(pk=temp_list.genre.pk)
        except:
            genre_music = None
        if list:
            return list.playlist_too().order_by('-created_at')
        elif tag_music:
            return tag_music.playlist_too()
        elif genre_music:
            return genre_music.playlist_too()
        else:
            return self.get_music()

    def get_docs_count(self):
        from docs.models import Doc2

        return Doc2.objects.filter(creator_id=self.pk, community__isnull=True).values("pk").count()

    def get_last_docs(self):
        from docs.models import DocList, Doc2

        docs_list = Doc2.objects.filter(creator_id=self.pk, community__isnull=True, is_deleted=False).exclude(type=Doc2.PRIVATE)[0:5]
        return docs_list[0:5]

    def is_doc_list_exists(self):
        return self.user_doclist.filter(creator_id=self.id, community__isnull=True, type="LI", is_deleted=False).exists()

    def get_docs_lists(self):
        from docs.models import DocList

        lists_query = Q(creator_id=self.id, community__isnull=True, type=DocList.LIST, is_deleted=False)
        return DocList.objects.filter(lists_query).order_by("order")

    def get_my_docs_lists(self):
        from docs.models import DocList

        lists_query = Q(creator_id=self.id, community__isnull=True, is_public=True, type=DocList.LIST, is_deleted=False)
        return DocList.objects.filter(lists_query).order_by("order")

    def get_all_docs_lists(self):
        from docs.models import DocList

        lists_query = Q(creator_id=self.id, community__isnull=True, is_deleted=False)
        return DocList.objects.filter(lists_query).order_by("order")

    def get_followers(self):
        followers_query = Q(follows__followed_user_id=self.pk)
        followers_query.add(~Q(Q(perm=User.DELETED) | Q(perm=User.BLOCKED) | Q(perm=User.PHONE_NO_VERIFIED)), Q.AND)
        return User.objects.filter(followers_query)

    def get_all_users(self):
        all_query = Q()
        all_query.add(~Q(Q(perm=User.DELETED)|Q(perm=User.BLOCKED)|Q(perm=User.PHONE_NO_VERIFIED)), Q.AND)
        if self.is_child():
            all_query.add(~Q(Q(perm=User.VERIFIED_SEND)|Q(perm=User.STANDART)), Q.AND)
        return User.objects.filter(all_query)

    def get_pop_followers(self):
        followers_query = Q(follows__followed_user_id=self.pk)
        followers_query.add(~Q(Q(perm=User.DELETED) | Q(perm=User.BLOCKED) | Q(perm=User.PHONE_NO_VERIFIED)), Q.AND)
        return User.objects.filter(followers_query)[0:6]

    def get_followings(self):
        followings_query = Q(followers__user_id=self.pk)
        followings_query.add(~Q(Q(perm=User.DELETED) | Q(perm=User.BLOCKED) | Q(perm=User.PHONE_NO_VERIFIED)), Q.AND)
        return User.objects.filter(followings_query)

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
        result=list(set([target_user['target_user_id'] for target_user in my_frends]) & set([target_user['target_user_id'] for target_user in user_frends]))
        query = Q(id__in=result)
        return User.objects.filter(query)

    def get_common_friends_of_community(self, community_id):
        from communities.models import Community

        community, my_frends = Community.objects.get(pk=community_id), self.connections.values('target_user_id')
        community_frends = community.memberships.values('user_id')
        result=list(set([target_user['target_user_id'] for target_user in my_frends]) & set([user_id['user_id'] for user_id in community_frends]))
        query = Q(id__in=result)
        return User.objects.filter(query)

    def get_common_friends_of_community_count_ru(self, community_id):
        from communities.models import Community

        community = Community.objects.get(pk=community_id)
        my_frends = self.connections.values('target_user_id')
        community_frends = community.memberships.values('user_id')
        my_frends_ids = [target_user['target_user_id'] for target_user in my_frends]
        community_frends_ids = [user_id['user_id'] for user_id in community_frends]
        result=list(set(my_frends_ids) & set(community_frends_ids))
        query = Q(id__in=result)
        count = User.objects.filter(query).values("pk").count()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return '{}{}'.format(str(count)," друг")
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return '{}{}'.format(str(count)," друга")
        else:
            return '{}{}'.format(str(count)," друзей")

    def get_target_users(self):
        from stst.models import UserNumbers
        query = []
        for user in [user['target'] for user in UserNumbers.objects.filter(visitor=self.pk).values('target').order_by("-count")]:
            query = query + [User.objects.get(id=user)]
        return query

    def get_last_visited_communities(self):
        from stst.models import CommunityNumbers
        from communities.models import Community
        v_s = CommunityNumbers.objects.filter(user=self.pk).values('community')
        result = list()
        map(lambda x: not x in result and result.append(x), [use['community'] for use in v_s])
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
        from communities.models import Community
        return CommunityNumbers.objects.filter(user=self.pk).distinct("community").values("community").count()


    def join_community(self, community_pk):
        from communities.models import Community
        from follows.models import CommunityFollow
        from invitations.models import CommunityInvite

        check_can_join_community(user=self, community_id=community_pk)
        community_to_join = Community.objects.get(pk=community_pk)
        community_to_join.add_member(self)
        if community_to_join.is_private():
            CommunityInvite.objects.filter(community_pk=community_pk, invited_user__id=self.id).delete()
        elif community_to_join.is_closed():
            CommunityFollow.objects.filter(community__pk=community_pk, user__id=self.id).delete()
        return community_to_join

    def leave_community(self, community_pk):
        from communities.models import Community

        check_can_leave_community(user=self, community_id=community_pk)
        community_to_leave = Community.objects.get(pk=community_pk)
        community_to_leave.remove_member(self)
        return community_to_leave

    def get_last_location(self):
        from users.model.profile import UserLocation
        try:
            return UserLocation.objects.filter(user_id=self.pk).last()
        except:
            return "Местоположение не указано"

    def get_sity_count(self, sity):
        from stst.models import UserNumbers
        from users.model.profile import UserLocation

        v_s = UserNumbers.objects.filter(target=self.pk).values('target')
        count = UserLocation.objects.filter(user_id__in=[use['target'] for use in v_s], city_ru=sity).count()
        return count

    ''''' модерация '''''
    def get_longest_user_penalties(self):
        return self.user_penalties.filter(user=self)[0].expiration
    def get_moderated_description(self):
        return self.moderated_user.filter(user=self)[0].description

    def get_moderation_users(self):
        # пользователи, на которых пожаловались
        from managers.model.user import ModeratedUser
        return ModeratedUser.objects.filter(verified=False)
    def get_penalty_users(self):
        # оштрафованные пользователи
        from managers.model.user import ModerationPenaltyUser
        return ModerationPenaltyUser.objects.filter(manager__id=self.pk)

    def get_moderation_communities(self):
        # сообщества, на которых пожаловались
        from managers.model.community import ModeratedCommunity
        return ModeratedCommunity.objects.filter(verified=False)
    def get_penalty_communities(self):
        # оштрафованные сообщества
        from managers.model.community import ModerationPenaltyCommunity
        return ModerationPenaltyCommunity.objects.filter(manager__id=self.pk)

    def get_moderation_posts(self):
        # записи, на которых пожаловались
        from managers.model.post import ModeratedPost
        return ModeratedPost.objects.filter(verified=False)
    def get_moderation_post_comments(self):
        # записи, на которых пожаловались
        from managers.model.post import ModeratedPostComment
        return ModeratedPostComment.objects.filter(verified=False)
    def get_penalty_posts(self):
        # оштрафованные записи
        from managers.model.post import ModerationPenaltyPost
        return ModerationPenaltyPost.objects.filter(manager__id=self.pk)
    def get_penalty_post_comments(self):
        # оштрафованные записи
        from managers.model.post import ModerationPenaltyPostComment
        return ModerationPenaltyPostComment.objects.filter(manager__id=self.pk)

    def get_moderation_photos(self):
        # записи, на которых пожаловались
        from managers.model.photo import ModeratedPhoto
        return ModeratedPhoto.objects.filter(verified=False)
    def get_moderation_photo_comments(self):
        # записи, на которых пожаловались
        from managers.model.photo import ModeratedPhotoComment
        return ModeratedPhotoComment.objects.filter(verified=False)
    def get_penalty_photos(self):
        # оштрафованные записи
        from managers.model.photo import ModerationPenaltyPhoto
        return ModerationPenaltyPhoto.objects.filter(manager__id=self.pk)
    def get_penalty_photo_comments(self):
        # оштрафованные записи
        from managers.model.photo import ModerationPenaltyPhotoComment
        return ModerationPenaltyPhotoComment.objects.filter(manager__id=self.pk)

    def get_moderation_goods(self):
        # записи, на которых пожаловались
        from managers.model.good import ModeratedGood
        return ModeratedGood.objects.filter(verified=False)
    def get_moderation_good_comments(self):
        # записи, на которых пожаловались
        from managers.model.good import ModeratedGoodComment
        return ModeratedGoodComment.objects.filter(verified=False)
    def get_penalty_goods(self):
        # оштрафованные записи
        from managers.model.good import ModerationPenaltyGood
        return ModerationPenaltyGood.objects.filter(manager__id=self.pk)
    def get_penalty_good_comments(self):
        # оштрафованные записи
        from managers.model.good import ModerationPenaltyGoodComment
        return ModerationPenaltyGoodComment.objects.filter(manager__id=self.pk)

    def get_moderation_videos(self):
        # записи, на которых пожаловались
        from managers.model.video import ModeratedVideo
        return ModeratedVideo.objects.filter(verified=False)
    def get_moderation_video_comments(self):
        # записи, на которых пожаловались
        from managers.model.video import ModeratedVideoComment
        return ModeratedVideoComment.objects.filter(verified=False)
    def get_penalty_videos(self):
        # оштрафованные записи
        from managers.model.video import ModerationPenaltyVideo
        return ModerationPenaltyVideo.objects.filter(manager__id=self.pk)
    def get_penalty_video_comments(self):
        # оштрафованные записи
        from managers.model.video import ModerationPenaltyVideoComment
        return ModerationPenaltyVideoComment.objects.filter(manager__id=self.pk)

    def get_moderation_audios(self):
        # записи, на которых пожаловались
        from managers.model.audio import ModeratedAudio
        return ModeratedAudio.objects.filter(verified=False)
    def get_penalty_audios(self):
        # оштрафованные записи
        from managers.model.audio import ModerationPenaltyAudio
        return ModerationPenaltyAudio.objects.filter(manager_id=self.pk)
    ''''' конец модерации '''''


    ''''' начало сообщения '''''

    def get_private_chats(self):
        from chat.models import Chat
        return Chat.objects.filter(chat_relation__user_id=self.pk, type=Chat.TYPE_PRIVATE, is_deleted=False)

    def get_all_chats(self):
        from chat.models import Chat
        return Chat.objects.filter(chat_relation__user_id=self.pk, is_deleted=False)

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
            if chat.chat_message.filter(is_deleted=False, unread=True).exclude(creator__user_id=self.pk).exists():
                count += 1
        if count > 0:
            return count
        else:
            return ''

    def get_user_notify(self):
        from notify.model.good import GoodNotify
        from notify.model.photo import PhotoNotify
        from notify.model.post import PostNotify
        from notify.model.user import UserNotify
        from notify.model.video import VideoNotify
        from itertools import chain

        return sorted(chain(UserNotify.objects.only('created').filter(recipient_id=self.pk), PostNotify.objects.only('created').filter(recipient_id=self.pk), PhotoNotify.objects.only('created').filter(recipient_id=self.pk), GoodNotify.objects.only('created').filter(recipient_id=self.pk), VideoNotify.objects.only('created').filter(recipient_id=self.pk)), key=lambda instance: instance.created, reverse=True)

    def read_user_notify(self):
        from notify.model.good import GoodNotify
        from notify.model.photo import PhotoNotify
        from notify.model.post import PostNotify
        from notify.model.user import UserNotify
        from notify.model.video import VideoNotify

        GoodNotify.notify_unread(self.pk)
        PhotoNotify.notify_unread(self.pk)
        PostNotify.notify_unread(self.pk)
        UserNotify.notify_unread(self.pk)
        VideoNotify.notify_unread(self.pk)

    def count_user_unread_notify(self):
        from notify.model.good import GoodNotify
        from notify.model.photo import PhotoNotify
        from notify.model.post import PostNotify
        from notify.model.user import UserNotify
        from notify.model.video import VideoNotify

        query = Q(recipient_id=self.pk, unread=True)
        return GoodNotify.objects.filter(query).values("pk").count() + PhotoNotify.objects.filter(query).values("pk").count() + PostNotify.objects.filter(query).values("pk").count() + UserNotify.objects.filter(query).values("pk").count() + VideoNotify.objects.filter(query).values("pk").count()

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
