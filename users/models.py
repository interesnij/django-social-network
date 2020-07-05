import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from common.checkers import *
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied


class User(AbstractUser):
    is_phone_verified = models.BooleanField(default=False, verbose_name='Телефон подтвержден')
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    is_manager = models.BooleanField(default=False, verbose_name="Доступен отдел для офицеров")
    is_supermanager = models.BooleanField(default=False, verbose_name="Доступен отдел для высших офицеров")
    is_suspended = models.BooleanField(default=False, verbose_name="Заморожен")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="uuid")
    last_activity= models.DateTimeField(default=timezone.now, blank=True, verbose_name='Активность')
    phone = models.CharField(max_length=17, unique=True, verbose_name='Телефон')
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_full_name(self):
        return  str(self.first_name) + " " + str(self.last_name)

    def create_s_avatar(self, photo_input):
        from users.model.profile import UserProfile
        from easy_thumbnails.files import get_thumbnailer
        try:
            user_profile = UserProfile.objects.get(user=self)
        except:
            user_profile = UserProfile.objects.create(user=self)
        user_profile.s_avatar = photo_input
        user_profile.save(update_fields=['s_avatar'])
        new_img = get_thumbnailer(user_profile.s_avatar)['small_avatar'].url.replace('media/', '')
        user_profile.s_avatar = new_img
        user_profile.save(update_fields=['s_avatar'])
        return user_profile.s_avatar

    def create_b_avatar(self, photo_input):
        from users.model.profile import UserProfile
        from easy_thumbnails.files import get_thumbnailer
        try:
            user_profile = UserProfile.objects.get(user=self)
        except:
            user_profile = UserProfile.objects.create(user=self)
        user_profile.b_avatar = photo_input
        user_profile.save(update_fields=['b_avatar'])
        new_img = get_thumbnailer(user_profile.b_avatar)['avatar'].url.replace('media/', '')
        user_profile.b_avatar = new_img
        user_profile.save(update_fields=['b_avatar'])
        return user_profile.b_avatar

    def get_b_avatar(self):
        from users.model.profile import UserProfile
        try:
            user_profile = UserProfile.objects.get(user=self)
            return user_profile.b_avatar.url
        except:
            return None

    def get_avatar(self):
        from users.model.profile import UserProfile
        try:
            user_profile = UserProfile.objects.get(user=self)
            return user_profile.s_avatar.url
        except:
            return None

    def get_online(self):
        from datetime import datetime, timedelta

        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=3)
        if now < onl:
            return True
        else:
            return False

    def get_request_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __str__(self):
        return self.get_full_name()

    def get_favorite_communities(self):
        return self.favorite_communities.all()

    def get_staffed_communities(self):
        from communities.models import Community

        query = Q(Q(memberships__user=self, memberships__is_administrator=True) | Q(memberships__user=self, memberships__is_moderator=True) | Q(memberships__user=self, memberships__is_editor=True))
        return Community.objects.filter(query)

        '''''проги для подписчиков  60-109'''''

    def follow_user(self, user):
        return self.follow_user_with_id(user.pk)

    def follow_user_with_id(self, user_id):
        from follows.models import Follow

        check_can_follow_user_with_id(user_id=user_id, user=self)
        if self.pk == user_id:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        follow = Follow.create_follow(user_id=self.pk, followed_user_id=user_id)
        return follow

    def community_follow_user(self, community_name):
        return self.follow_community_with_name(community_name)

    def follow_community_with_name(self, community_name):
        from follows.models import CommunityFollow

        check_can_join_community_with_name(user=self, community_name=community_name)
        follow = CommunityFollow.create_follow(user_id=self.pk, community_name=community_name)
        return follow

    def community_unfollow_user(self, community_name):
        return self.unfollow_community_with_name(community_name)

    def unfollow_community_with_name(self, community_name):
        from follows.models import CommunityFollow

        check_can_join_community_with_name(user=self, community_name=community_name)
        follow = CommunityFollow.objects.get(user=self,community=community_name)
        follow.delete()

    def frend_user(self, user):
        return self.frend_user_with_id(user.pk)

    def frend_user_with_id(self, user_id):
        from follows.models import Follow
        from frends.models import Connect

        check_can_connect_with_user_with_id(user=self, user_id=user_id)
        if self.pk == user_id:
            raise ValidationError('Вы не можете добавить сами на себя',)
        frend = Connect.create_connection(user_id=self.pk, target_user_id=user_id)
        follow = Follow.objects.get(user=user_id, followed_user_id=self.pk)
        follow.delete()
        return frend

    def unfollow_user(self, user):
        return self.unfollow_user_with_id(user.pk)

    def unfollow_user_with_id(self, user_id):
        from follows.models import Follow

        check_not_can_follow_user_with_id(user=self, user_id=user_id)
        follow = Follow.objects.get(user=self,followed_user=user_id)
        follow.delete()

    def unfrend_user(self, user):
        return self.unfrend_user_with_id(user.pk)

    def unfrend_user_with_id(self, user_id):
        from follows.models import Follow

        check_is_following_user_with_id(user=self, user_id=user_id)
        follow = Follow.create_follow(user_id=user_id, followed_user_id=self.pk)
        connection = self.connections.get(target_connection__user_id=user_id)
        connection.delete()

    def unblock_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        return self.unblock_user_with_id(user_id=user.pk)

    def unblock_user_with_id(self, user_id):
        check_can_unblock_user_with_id(user=self, user_id=user_id)
        self.user_blocks.filter(blocked_user_id=user_id).delete()
        return User.objects.get(pk=user_id)

    def block_user_with_pk(self, pk):
        user = User.objects.get(pk=pk)
        return self.block_user_with_id(user_id=user.pk)

    def block_user_with_id(self, user_id):
        from users.model.list import UserBlock
        check_can_block_user_with_id(user=self, user_id=user_id)

        if self.is_connected_with_user_with_id(user_id=user_id):
            self.disconnect_from_user_with_id(user_id=user_id)
        elif self.is_following_user_with_id(user_id=user_id):
            self.unfollow_user_with_id(user_id=user_id)

        user_to_block = User.objects.get(pk=user_id)
        if user_to_block.is_following_user_with_id(user_id=self.pk):
            user_to_block.unfollow_user_with_id(self.pk)

        UserBlock.create_user_block(blocker_id=self.pk, blocked_user_id=user_id)
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

    def _make_followers_query(self):
        return Q(follows__followed_user_id=self.pk, is_deleted=False)

    def _make_followings_query(self):
        return Q(followers__user_id=self.pk, is_deleted=False)


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

    def is_pending_confirm_connection_for_user_with_id(self, user_id):
        if not self.is_connected_with_user_with_id(user_id):
            return False
        connection = self.connections.filter(target_connection__user_id=user_id).get()
        return not connection.circles.exists()

    def is_global_moderator(self):
        moderators_community_name = settings.MODERATORS_COMMUNITY_NAME
        return self.is_member_of_community_with_name(community_name=moderators_community_name)

    def is_invited_to_community_with_name(self, community_name):
        from communities.models import Community

        return Community.is_user_with_username_invited_to_community_with_name(username=self.username, community_name=community_name)

    def is_staff_of_community_with_name(self, community_name):
        return self.is_administrator_of_community_with_name(community_name=community_name) or self.is_moderator_of_community_with_name(community_name=community_name) or self.is_editor_of_community_with_name(community_name=community_name)

    def is_member_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name).exists()

    def is_banned_from_community_with_name(self, community_name):
        return self.banned_of_communities.filter(name=community_name).exists()

    def is_star_from_community_with_name(self, community_name):
        return self.favorite_communities.filter(name=community_name).exists()

    def is_follow_from_community_with_name(self, community_pk):
        from follows.models import CommunityFollow

        try:
            return CommunityFollow.objects.get(community__id=community_pk, user=self).exists()
        except:
            return False

    def is_closed_profile(self):
        from users.model.settings import UserPrivate

        try:
            user_private = UserPrivate.objects.get(user=self)
            return user_private.is_private
        except:
            user_private = UserPrivate.objects.create(user=self)
            return False

    def is_creator_of_community_with_name(self, community_name):
        return self.created_communities.filter(name=community_name).exists()

    def is_staffed_user(self):
        return self.communities_memberships.filter(Q(is_administrator=True) | Q(is_moderator=True) | Q(is_editor=True)).exists()

    def is_staff_of_community_with_name(self, community_name):
        return self.is_administrator_of_community_with_name(community_name=community_name) or self.is_moderator_of_community_with_name(community_name=community_name) or self.is_editor_of_community_with_name(community_name=community_name) or self.is_advertiser_of_community_with_name(community_name=community_name)

    def is_administrator_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_administrator=True).exists()

    def is_moderator_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_moderator=True).exists()

    def is_advertiser_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_advertiser=True).exists()

    def is_editor_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_editor=True).exists()

    def is_following_user_with_id(self, user_id):
        return self.follows.filter(followed_user__id=user_id).exists()

    def is_followers_user_with_id(self, user_id):
        return self.follows.filter(user__id=user_id).exists()

    def is_album_exists(self):
        return self.created_user.filter(creator__id=self.pk, community=None).exists()

    def is_photo_exists(self):
        return self.photo_creator.filter(creator__id=self.pk, community=None).exists()

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
        try:
            if self.user_staff.level == "A":
                return True
        except:
            return False
    def is_user_moderator(self):
        try:
            if self.user_staff.level == "M":
                return True
        except:
            return False
    def is_user_editor(self):
        try:
            if self.user_staff.level == "E":
                return True
        except:
            return False
    def is_user_advertiser(self):
        try:
            if self.user_staff.level == "R":
                return True
        except:
            return False
    def is_user_manager(self):
        try:
            if self.user_staff.level and self.user_staff.level != "R":
                return True
        except:
            return False

    def is_community_administrator(self):
        try:
            if self.user_community_staff.level == "A":
                return True
        except:
            return False
    def is_community_moderator(self):
        try:
            if self.user_community_staff.level == "M":
                return True
        except:
            return False
    def is_community_editor(self):
        try:
            if self.user_community_staff.level == "E":
                return True
        except:
            return False
    def is_community_advertiser(self):
        try:
            if self.user_community_staff.level == "R":
                return True
        except:
            return False
    def is_community_manager(self):
        try:
            if self.user_community_staff.level and self.user_community_staff.level != "R":
                return True
        except:
            return False

    def is_post_administrator(self):
        try:
            if self.post_user_staff.level == "A":
                return True
        except:
            return False
    def is_post_moderator(self):
        try:
            if self.post_user_staff.level == "M":
                return True
        except:
            return False
    def is_post_editor(self):
        try:
            if self.post_user_staff.level == "E":
                return True
        except:
            return False
    def is_post_manager(self):
        try:
            if self.post_user_staff.level:
                return True
        except:
            return False

    def is_good_administrator(self):
        try:
            if self.good_user_staff.level == "A":
                return True
        except:
            return False
    def is_good_moderator(self):
        try:
            if self.good_user_staff.level == "M":
                return True
        except:
            return False
    def is_good_editor(self):
        try:
            if self.good_user_staff.level == "E":
                return True
        except:
            return False
    def is_good_manager(self):
        try:
            if self.good_user_staff.level:
                return True
        except:
            return False

    def is_photo_administrator(self):
        try:
            if self.photo_user_staff.level == "A":
                return True
        except:
            return False
    def is_photo_moderator(self):
        try:
            if self.photo_user_staff.level == "M":
                return True
        except:
            return False
    def is_photo_editor(self):
        try:
            if self.photo_user_staff.level == "E":
                return True
        except:
            return False
    def is_photo_manager(self):
        try:
            if self.photo_user_staff.level:
                return True
        except:
            return False

    def is_video_administrator(self):
        try:
            if self.video_user_staff.level == "A":
                return True
        except:
            return False
    def is_video_moderator(self):
        try:
            if self.video_user_staff.level == "M":
                return True
        except:
            return False
    def is_video_editor(self):
        try:
            if self.video_user_staff.level == "E":
                return True
        except:
            return False
    def is_video_manager(self):
        try:
            if self.video_user_staff.level:
                return True
        except:
            return False

    def is_audio_administrator(self):
        try:
            if self.audio_user_staff.level == "A":
                return True
        except:
            return False
    def is_audio_moderator(self):
        try:
            if self.audio_user_staff.level == "M":
                return True
        except:
            return False
    def is_audio_editor(self):
        try:
            if self.audio_user_staff.level == "E":
                return True
        except:
            return False
    def is_audio_manager(self):
        try:
            if self.audio_user_staff.level:
                return True
        except:
            return False

    def is_work_administrator(self):
        try:
            if self.can_work_staff_user.can_work_administrator:
                return True
        except:
            return False
    def is_work_moderator(self):
        try:
            if self.can_work_staff_user.can_work_moderator:
                return True
        except:
            return False
    def is_work_editor(self):
        try:
            if self.can_work_staff_user.can_work_editor:
                return True
        except:
            return False
    def is_work_advertiser(self):
        try:
            if self.can_work_staff_user.can_work_advertiser:
                return True
        except:
            return False
    def is_user_supermanager(self):
        try:
            if self.can_work_staff_user.level:
                return True
        except:
            return False

    def is_work_community_administrator(self):
        try:
            if self.can_work_staff_community.can_work_administrator:
                return True
        except:
            return False
    def is_work_community_moderator(self):
        try:
            if self.can_work_staff_community.can_work_moderator:
                return True
        except:
            return False
    def is_work_community_editor(self):
        try:
            if self.can_work_staff_community.can_work_editor:
                return True
        except:
            return False
    def is_work_community_advertiser(self):
        try:
            if self.can_work_staff_community.can_work_advertiser:
                return True
        except:
            return False
    def is_community_supermanager(self):
        try:
            if self.can_work_staff_community.level:
                return True
        except:
            return False

    def is_work_post_administrator(self):
        try:
            if self.can_work_staff_post_user.can_work_administrator:
                return True
        except:
            return False
    def is_work_post_moderator(self):
        try:
            if self.can_work_staff_post_user.can_work_moderator:
                return True
        except:
            return False
    def is_work_post_editor(self):
        try:
            if self.can_work_staff_post_user.can_work_editor:
                return True
        except:
            return False
    def is_work_supermanager(self):
        try:
            if self.can_work_staff_post_user.level:
                return True
        except:
            return False

    def is_work_good_administrator(self):
        try:
            if self.can_work_staff_good_user.can_work_administrator:
                return True
        except:
            return False
    def is_work_good_moderator(self):
        try:
            if self.can_work_staff_good_user.can_work_moderator:
                return True
        except:
            return False
    def is_work_good_editor(self):
        try:
            if self.can_work_staff_good_user.can_work_editor:
                return True
        except:
            return False
    def is_work_supermanager(self):
        try:
            if self.can_work_staff_good_user.level:
                return True
        except:
            return False

    def is_work_photo_administrator(self):
        try:
            if self.can_work_staff_photo_user.can_work_administrator:
                return True
        except:
            return False
    def is_work_photo_moderator(self):
        try:
            if self.can_work_staff_photo_user.can_work_moderator:
                return True
        except:
            return False
    def is_work_photo_editor(self):
        try:
            if self.can_work_staff_photo_user.can_work_editor:
                return True
        except:
            return False
    def is_photo_supermanager(self):
        try:
            if self.can_work_staff_photo_user.level:
                return True
        except:
            return False

    def is_work_video_administrator(self):
        try:
            if self.can_work_staff_video_user.can_work_administrator:
                return True
        except:
            return False
    def is_work_video_moderator(self):
        try:
            if self.can_work_staff_video_user.can_work_moderator:
                return True
        except:
            return False
    def is_work_video_editor(self):
        try:
            if self.can_work_staff_video_user.can_work_editor:
                return True
        except:
            return False
    def is_video_supermanager(self):
        try:
            if self.can_work_staff_video_user.level:
                return True
        except:
            return False

    def is_work_music_administrator(self):
        try:
            if self.can_work_staff_music_user.can_work_administrator:
                return True
        except:
            return False
    def is_work_music_moderator(self):
        try:
            if self.can_work_staff_music_user.can_work_moderator:
                return True
        except:
            return False
    def is_work_music_editor(self):
        try:
            if self.can_work_staff_music_user.can_work_editor:
                return True
        except:
            return False
    def is_music_supermanager(self):
        try:
            if self.can_work_staff_music_user.level:
                return True
        except:
            return False

    ''''' количества всякие  196-216 '''''

    def count_followers(self):
        return self.follows.values('pk').count()

    def count_following(self):
        return self.followers.values('pk').count()

    def count_connections(self):
        return self.connections.values('pk').count()

    def count_community(self):
        return self.communities_memberships.values('pk').count()

    def count_photos(self):
        return self.photo_creator.values('pk').count()

    def count_albums(self):
        return self.created_user.values('pk').count()

    def count_goods(self):
        return self.good_creator.values('pk').count()

    def count_posts(self):
        return self.posts.values('pk').count()


    ''''' GET всякие  219-186 '''''
    def get_pop_connection(self):
        from managers.model.user import ModeratedUser

        my_frends = self.connections.values('target_user_id')
        my_frends_ids = [target_user['target_user_id'] for target_user in my_frends]
        connection_query = Q(id__in=my_frends_ids)
        #exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #connection_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        connection_query.add(~Q(Q(blocked_by_users__blocker_id=self.id) | Q(user_blocks__blocked_user_id=self.id)), Q.AND)
        frends = User.objects.filter(connection_query)
        return frends[0:5]

    def get_all_connection(self):
        from managers.model.user import ModeratedUser

        my_frends = self.connections.values('target_user_id')
        my_frends_ids = [target_user['target_user_id'] for target_user in my_frends]
        connection_query = Q(id__in=my_frends_ids)
        #exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #connection_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        connection_query.add(~Q(Q(blocked_by_users__blocker_id=self.id) | Q(user_blocks__blocked_user_id=self.id)), Q.AND)
        frends = User.objects.filter(connection_query)
        return frends

    def get_online_connection(self):
        frends = self.get_all_connection()
        query = []
        for frend in frends:
            if frend.get_online():
                query += [frend,]
        return query

    def get_pop_communities(self):
        from communities.models import Community

        query = Q(memberships__user=self)
        communities = Community.objects.filter(query)
        return communities[0:6]

    def get_online_connection_count(self):
        frends = self.get_all_connection()
        query = []
        for frend in frends:
            if frend.get_online():
                query += [frend,]
        return len(query)

    def get_pop_online_connection(self):
        frends = self.get_all_connection()
        query = []
        for frend in frends:
            if frend.get_online():
                query += [frend,]
        return query[0:5]

    def get_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_query = Q(creator_id=self.id, is_deleted=False, is_fixed=False, status=Post.STATUS_PUBLISHED, community=None)
        #exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #posts_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        posts = Post.objects.filter(posts_query)
        return posts
    def get_draft_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_query = Q(creator_id=self.id, is_deleted=False, is_fixed=False, status=Post.STATUS_DRAFT, community=None)
        #exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #posts_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        posts = Post.objects.filter(posts_query)
        return posts
    def get_archive_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_query = Q(creator_id=self.id, is_deleted=False, is_fixed=False, status=Post.STATUS_ARHIVED, community=None)
        #exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #posts_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        posts = Post.objects.filter(posts_query)
        return posts

    def get_articles(self):
        from article.models import Article
        from managers.model.post import ModeratedPost

        articles_query = Q(creator_id=self.id, is_deleted=False)
        #exclude_reported_and_approved_articles_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #articles_query.add(exclude_reported_and_approved_articles_query, Q.AND)
        articles = Article.objects.filter(articles_query)
        return articles

    def get_photos(self):
        from gallery.models import Photo
        from managers.model.photo import ModeratedPhoto

        photos_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community=None)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos

    def get_profile_photos(self):
        from gallery.models import Photo
        from managers.model.photo import ModeratedPhoto

        photos_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community=None)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos[0:6]

    def get_my_photos(self):
        from gallery.models import Photo
        from managers.model.photo import ModeratedPhoto

        photos_query = Q(creator_id=self.id, is_deleted=False, community=None)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos

    def get_photos_for_album(self, album_id):
        from gallery.models import Photo
        from managers.model.photo import ModeratedPhoto

        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        photos_query = Q(album__pk=album_id, is_deleted=False, is_public=True)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos
    def get_photos_for_my_album(self, album_id):
        from gallery.models import Photo
        from managers.model.photo import ModeratedPhoto

        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        photos_query = Q(album__id=album_id, is_deleted=False)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos

    def get_avatar_photos(self):
        from gallery.models import Photo
        from managers.model.photo import ModeratedPhoto

        photos_query = Q(creator_id=self.id, is_deleted=False, album__title="Фото со страницы", album__is_generic=True, album__community=None)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        avatar_photos = Photo.objects.filter(photos_query)
        return avatar_photos

    def get_albums(self):
        from gallery.models import Album
        from managers.model.photo import ModeratedPhoto

        albums_query = Q(creator_id=self.id, is_deleted=False, is_public=True, is_generic=False, community=None)
        #exclude_reported_and_approved_albums_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #albums_query.add(exclude_reported_and_approved_albums_query, Q.AND)
        albums = Album.objects.filter(albums_query)
        return albums

    def get_my_albums(self):
        from gallery.models import Album
        from managers.model.photo import ModeratedPhoto

        albums_query = Q(creator_id=self.id, is_deleted=False, community=None)
        #exclude_reported_and_approved_albums_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #albums_query.add(exclude_reported_and_approved_albums_query, Q.AND)
        albums = Album.objects.filter(albums_query)
        return albums

    def get_video_albums(self):
        from video.models import VideoAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community=None)
        albums = VideoAlbum.objects.filter(albums_query)
        return albums

    def my_user_video_album_exists(self):
        return self.video_user_creator.filter(creator_id=self.id, is_generic=False).exists()
    def user_video_album_exists(self):
        return self.video_user_creator.filter(creator_id=self.id, is_public=True, is_generic=False).exists()
    def user_music_playlist_exists(self):
        return self.user_playlist.filter(creator_id=self.id, is_generic=False).exists()

    def get_my_video_albums(self):
        from video.models import VideoAlbum

        albums_query = Q(creator_id=self.id, is_deleted=False, community=None, is_generic=False)
        albums = VideoAlbum.objects.filter(albums_query)
        return albums

    def get_audio_playlists(self):
        from music.models import SoundList

        playlists_query = Q(creator_id=self.id, community=None, is_generic=False)
        playlists = SoundList.objects.filter(playlists_query)
        return playlists

    def get_goods(self):
        from goods.models import Good

        goods_query = Q(creator_id=self.id, is_deleted=False, status=Good.STATUS_PUBLISHED)
        goods = Good.objects.filter(goods_query)
        return goods
    def get_my_goods(self):
        from goods.models import Good

        goods_query = Q(creator_id=self.id, is_deleted=False)
        goods = Good.objects.filter(goods_query)
        return goods

    def get_music(self):
        from music.models import SoundList, SoundcloudParsing
        try:
            list = SoundList.objects.get(creator_id=self.id, community=None, is_generic=True, name="Основной плейлист")
        except:
            list = SoundList.objects.create(creator_id=self.id, community=None, is_generic=True, name="Основной плейлист")
        music_query = list.players.filter(is_deleted=False)
        #music_list = SoundcloudParsing.objects.filter(music_query)
        return music_query

    def get_music_count(self):
        from music.models import SoundList, SoundcloudParsing

        list = SoundList.objects.get(creator_id=self.id, community=None, is_generic=True)
        music_query = Q(list=list, is_deleted=False)
        count = SoundcloudParsing.objects.filter(music_query).values("pk")
        return count.count()

    def get_last_music(self):
        lists = []
        i = 1
        for music in self.get_music():
            if i < 6:
                lists += [music,]
                i += 1
        return lists

    def get_video_count(self):
        from video.models import Video, VideoAlbum

        list = VideoAlbum.objects.get(creator_id=self.id, community=None, is_generic=True, title="Все видео")
        video_query = Q(album=list, is_deleted=False)
        count = Video.objects.filter(video_query).values("pk")
        return count.count()

    def get_video(self):
        from video.models import Video, VideoAlbum
        try:
            list = VideoAlbum.objects.get(creator_id=self.id, is_generic=True, title="Все видео")
        except:
            list = VideoAlbum.objects.create(creator_id=self.id, is_generic=True, title="Все видео")
        video_query = Q(album=list, is_deleted=False, is_public=True)
        video_list = Video.objects.filter(video_query).order_by("-created")
        return video_list

    def get_my_video(self):
        from video.models import Video, VideoAlbum
        try:
            list = VideoAlbum.objects.get(creator_id=self.id, community=None, is_generic=True, title="Все видео")
        except:
            list = VideoAlbum.objects.create(creator_id=self.id, is_generic=True, title="Все видео")
        video_query = Q(album=list, is_deleted=False)
        video_list = Video.objects.filter(video_query).order_by("-created")
        return video_list

    def get_last_video(self):
        from video.models import Video, VideoAlbum
        try:
            list = VideoAlbum.objects.get(creator_id=self.id, community=None, is_generic=True, title="Все видео")
        except:
            list = VideoAlbum.objects.create(creator_id=self.id, community=None, is_generic=True, title="Все видео")
        video_query = Q(album=list, is_deleted=False, is_public=True)
        video_list = Video.objects.filter(video_query).order_by("-created")
        return video_list[0:2]

    def get_all_video_list_uuid(self):
        from video.models import VideoAlbum
        try:
            album = VideoAlbum.objects.get(creator_id=self.id, community=None, is_generic=True, title="Все видео")
        except:
            album = VideoAlbum.objects.create(creator_id=self.id, community=None, is_generic=True, title="Все видео")
        return album.uuid

    def get_music_list_id(self):
        from music.models import SoundList
        try:
            list = SoundList.objects.get(creator_id=self.id, community=None, is_generic=True, name="Основной плейлист")
        except:
            list = SoundList.objects.create(creator_id=self.id, community=None, is_generic=True, name="Основной плейлист")
        return list.pk

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
            return list.playlist_too()
        elif tag_music:
            return tag_music.playlist_too()
        elif genre_music:
            return genre_music.playlist_too()
        else:
            queryset = self.get_music()
            return queryset

    def get_avatar_uuid(self):
        avatar = self.get_avatar_photos().order_by('-id')[0]
        return avatar.uuid

    def get_followers(self):
        followers_query = self._make_followers_query()
        return User.objects.filter(followers_query)

    def get_pop_followers(self):
        followers_query = self._make_followers_query()
        return User.objects.filter(followers_query)[0:6]

    def get_followings(self):
        followings_query = self._make_followings_query()
        return User.objects.filter(followings_query)

    def get_timeline_posts(self):
        return self._get_timeline_posts_v2()

    def _get_timeline_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_select_related = ('creator', 'community')
        posts_only = ('id', 'created', 'creator__id', 'community__id')
        #reported_posts_exclusion_query = ~Q(moderated_object__reports__reporter_id=self.pk)
        own_posts_query = Q(creator=self.pk, community__isnull=True, is_deleted=False, status=Post.STATUS_PUBLISHED)
        own_posts_query.add(reported_posts_exclusion_query, Q.AND)
        own_posts_queryset = self.posts.select_related(*posts_select_related).only(*posts_only).filter(own_posts_query)

        community_posts_query = Q(community__memberships__user__id=self.pk, is_closed=False, is_deleted=False, status=Post.STATUS_PUBLISHED)
        community_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(creator__user_blocks__blocked_user_id=self.pk)), Q.AND)
        #community_posts_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
        #community_posts_query.add(reported_posts_exclusion_query, Q.AND)
        community_posts_queryset = Post.objects.select_related(*posts_select_related).only(*posts_only).filter(community_posts_query)

        followed_users = self.follows.values('followed_user_id')
        followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
        followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, status=Post.STATUS_PUBLISHED)
        #followed_users_query.add(reported_posts_exclusion_query, Q.AND)
        followed_users_queryset = Post.objects.select_related(*posts_select_related).only(*posts_only).filter(followed_users_query)

        frends = self.connections.values('target_user_id')
        frends_ids = [target_user['target_user_id'] for target_user in frends]
        frends_query = Q(creator__in=frends_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
        #frends_query.add(reported_posts_exclusion_query, Q.AND)
        frends_queryset = Post.objects.select_related(*posts_select_related).only(*posts_only).filter(frends_query)
        final_queryset = own_posts_queryset.union(community_posts_queryset, followed_users_queryset, frends_queryset)
        return final_queryset

    def _get_timeline_posts_v2(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        #reported_posts_exclusion_query = ~Q(moderated_object__reports__reporter_id=self.pk)
        own_posts_query = Q(creator=self.pk, community__isnull=True, is_deleted=False, status=Post.STATUS_PUBLISHED)
        #own_posts_query.add(reported_posts_exclusion_query, Q.AND)
        own_posts_queryset = self.post_creator.only('created').filter(own_posts_query)

        community_posts_query = Q(community__memberships__user__id=self.pk, is_deleted=False, status=Post.STATUS_PUBLISHED)
        community_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(creator__user_blocks__blocked_user_id=self.pk)), Q.AND)
        #community_posts_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
        #community_posts_query.add(reported_posts_exclusion_query, Q.AND)
        community_posts_queryset = Post.objects.only('created').filter(community_posts_query)

        followed_users = self.follows.values('followed_user_id')
        followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
        followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, status=Post.STATUS_PUBLISHED)
        #followed_users_query.add(reported_posts_exclusion_query, Q.AND)
        followed_users_queryset = Post.objects.only('created').filter(followed_users_query)

        frends = self.connections.values('target_user_id')
        frends_ids = [target_user['target_user_id'] for target_user in frends]
        frends_query = Q(creator__in=frends_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
        #frends_query.add(reported_posts_exclusion_query, Q.AND)
        frends_queryset = Post.objects.only('created').filter(frends_query)
        final_queryset = own_posts_queryset.union(community_posts_queryset, followed_users_queryset, frends_queryset)
        return final_queryset

    def get_follows(self):
        #reported_posts_exclusion_query = ~Q(moderated_object__reports__reporter_id=self.pk)
        followed_users = self.followers.values('user_id')
        followed_users_ids = [followed_user['user_id'] for followed_user in followed_users]
        followed_users_query = Q(id__in=followed_users_ids)
        #followed_users_query.add(reported_posts_exclusion_query, Q.AND)
        query = User.objects.filter(followed_users_query)
        return query

    def get_possible_friends(self):
        frends = self.connections.values('target_user_id')
        if not frends:
            return "not frends"
        frends_ids = [target_user['target_user_id'] for target_user in frends]
        query = Q()
        for frend in frends_ids:
            user = User.objects.get(pk=frend)
            frends_frends = user.connections.values('target_user_id')
            frend_frend_ids = [target_user['target_user_id'] for target_user in frends_frends]
            _query = Q(id__in=frend_frend_ids)
            blocked = ~Q(Q(blocked_by_users__blocker_id=self.pk) | Q(user_blocks__blocked_user_id=self.pk))
            connections = ~Q(Q(connections__user_id=self.pk) | Q(targeted_connections__target_user_id=self.pk))
            _query.add(blocked, Q.AND)
            _query.add(connections, Q.AND)
            query.add(_query, Q.AND)
        connection = User.objects.filter(query)
        return connection

    def get_possible_friends_10(self):
        frends = self.connections.values('target_user_id')
        if not frends:
            return False
        frends_ids = [target_user['target_user_id'] for target_user in frends]
        query = Q()
        for frend in frends_ids:
            user = User.objects.get(pk=frend)
            frends_frends = user.connections.values('target_user_id')
            frend_frend_ids = [target_user['target_user_id'] for target_user in frends_frends]
            _query = Q(id__in=frend_frend_ids)
            blocked = ~Q(Q(blocked_by_users__blocker_id=self.pk) | Q(user_blocks__blocked_user_id=self.pk))
            connections = ~Q(Q(connections__user_id=self.pk) | Q(targeted_connections__target_user_id=self.pk))
            _query.add(blocked, Q.AND)
            _query.add(connections, Q.AND)
            query.add(_query, Q.AND)
        connection = User.objects.filter(query)
        return connection[0:10]

    def get_common_friends_of_user(self, user):
        user = User.objects.get(pk=user.pk)
        if self.pk == user.pk:
            return ""
        my_frends = self.connections.values('target_user_id')
        user_frends = user.connections.values('target_user_id')
        my_frends_ids = [target_user['target_user_id'] for target_user in my_frends]
        user_frend_ids = [target_user['target_user_id'] for target_user in user_frends]
        result=list(set(my_frends_ids) & set(user_frend_ids))
        query = Q(id__in=result)
        connection = User.objects.filter(query)
        return connection

    def get_common_friends_of_community(self, community_id):
        from communities.models import Community

        community = Community.objects.get(pk=community_id)
        my_frends = self.connections.values('target_user_id')
        community_frends = community.memberships.values('user_id')
        my_frends_ids = [target_user['target_user_id'] for target_user in my_frends]
        community_frends_ids = [user_id['user_id'] for user_id in community_frends]
        result=list(set(my_frends_ids) & set(community_frends_ids))
        query = Q(id__in=result)
        connection = User.objects.filter(query)
        return connection

    def get_template_user(self, folder, template, request):
        import re

        if self.pk == request.user.pk:
            if not request.user.is_phone_verified:
                template_name = "main/phone_verification.html"
            elif self.is_suspended():
                self.template_name = "main/you_suspended.html"
            elif self.is_blocked():
                self.template_name = "main/you_global_block.html"
            else:
                template_name = folder + "my_" + template
        elif request.user.pk != self.pk and request.user.is_authenticated:
            if not request.user.is_phone_verified:
                template_name = "main/phone_verification.html"
            elif self.is_suspended():
                self.template_name = "main/user_suspended.html"
            elif self.is_blocked():
                self.template_name = "main/user_global_block.html"
            elif self.is_have_warning_banner():
                self.template_name = "account/user_have_warning_banner.html"
            elif request.user.is_blocked_with_user_with_id(user_id=self.pk):
                template_name = folder + "block_" + template
            elif self.is_closed_profile():
                if not request.user.is_connected_with_user_with_id(user_id=self.pk):
                    template_name = folder + "close_" + template
                else:
                    template_name = folder + "frend_" + template
            else:
                template_name = folder + template
        elif request.user.is_anonymous and self.is_closed_profile():
            template_name = folder + "close_" + template
        elif request.user.is_anonymous and not self.is_closed_profile():
            template_name = folder + "anon_" + template
        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_template_list_user(self, folder, template, request):
        import re

        if self.pk == request.user.pk:
            template_name = folder + "my_" + template
        elif self != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.id)
            template_name = folder + template
            if self.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.id)
                template_name = folder + template
        elif request.user.is_anonymous and not self.is_closed_profile():
            template_name = folder + "anon_" + template
        elif request.user.is_anonymous and self.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')

        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_permission_list_user(self, folder, template, request):
        import re

        if self.pk == request.user.pk:
            template_name = folder + "my_" + template
        elif self != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.id)
            template_name = folder + template
            if self.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.id)
                template_name = folder + template
        elif request.user.is_anonymous and not self.is_closed_profile():
            template_name = folder + template
        elif request.user.is_anonymous and self.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')

        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_settings_template(self, folder, template, request):
        import re

        template_name = folder + template

        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_target_users(self):
        from stst.models import UserNumbers
        v_s = UserNumbers.objects.filter(visitor=self.pk).values('target').order_by("-count")
        ids = [user['target'] for user in v_s]
        query = []
        for user in ids:
            query = query + [User.objects.get(id=user), ]
        return query

    def get_last_visited_communities(self):
        from stst.models import CommunityNumbers
        from communities.models import Community
        v_s = CommunityNumbers.objects.filter(user=self.pk).values('community')
        ids = [use['community'] for use in v_s]
        result = list()
        map(lambda x: not x in result and result.append(x), ids)
        query = []
        for i in result:
            query = query + [Community.objects.get(id=i), ]
        return query

    def get_visited_communities(self):
        from stst.models import CommunityNumbers
        from communities.models import Community
        v_s = CommunityNumbers.objects.filter(user=self.pk).values("community")
        ids = [use['community'] for use in v_s]
        result = list()
        map(lambda x: not x in result and result.append(x), ids)
        query = []
        for i in result:
            query = query + [Community.objects.get(id=i), ]
        return query


    def join_community_with_name(self, community_name):
        from communities.models import Community
        from follows.models import CommunityFollow
        from invitations.models import CommunityInvite

        check_can_join_community_with_name(user=self, community_name=community_name)
        community_to_join = Community.objects.get(name=community_name)
        community_to_join.add_member(self)
        if community_to_join.is_private():
            CommunityInvite.objects.filter(community_name=community_name, invited_user__id=self.id).delete()
        elif community_to_join.is_closed():
            CommunityFollow.objects.filter(community__name=community_name, user__id=self.id).delete()
        return community_to_join

    def leave_community_with_name(self, community_name):
        from communities.models import Community

        check_can_leave_community_with_name(user=self, community_name=community_name)
        community_to_leave = Community.objects.get(name=community_name)
        community_to_leave.remove_member(self)
        return community_to_leave

    def has_blocked_user_with_id(self, user_id):
        return self.user_blocks.filter(blocked_user_id=user_id).exists()

    def get_last_location(self):
        from users.model.profile import OneUserLocation, TwoUserLocation, ThreeUserLocation
        if self.user_ip.ip_3:
            return ThreeUserLocation.objects.get(user=self)
        elif self.user_ip.ip_2:
            return TwoUserLocation.objects.get(user=self)
        elif self.user_ip.ip_1:
            return OneUserLocation.objects.get(user=self)
        else:
            return "Местоположение не указано"

    def get_sity_count(self, sity):
        from stst.models import UserNumbers
        from users.model.profile import OneUserLocation

        v_s = UserNumbers.objects.filter(target=self.pk).values('target')
        ids = [use['target'] for use in v_s]
        count = OneUserLocation.objects.filter(user_id__in=ids, city_ru=sity).count()
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
    def get_penalty_posts(self):
        # оштрафованные записи
        from managers.model.post import ModerationPenaltyPost
        return ModerationPenaltyPost.objects.filter(manager__id=self.pk)
    ''''' конец модерации '''''
