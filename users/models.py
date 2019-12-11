from datetime import datetime, timedelta
import uuid
from django.utils import six, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community
from follows.models import Follow, CommunityFollow
from goods.models import Good
from frends.models import Connect
from posts.models import Post
from common.models import ItemVotes
from gallery.models import Photo, Album
from moderation.models import ModeratedObject, ModerationPenalty
from common.checkers import *
from django.db.models import Q, F, Count


class User(AbstractUser):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='users')
    is_email_verified = models.BooleanField(default=False)
    are_guidelines_accepted = models.BooleanField(default=False)
    is_deleted = models.BooleanField(
        verbose_name="Удален",
        default=False,
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="uuid")
    last_activity= models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Активность')



    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_full_name(self):
        return  str(self.first_name) + " " + str(self.last_name)

    def get_online(self):
        now = datetime.now()
        onl = self.last_activity + timedelta(minutes=1)
        if now < onl:
            return True
        else:
            return False

    def __str__(self):
        return self.get_full_name()

    def get_favorite_communities(self):
        return self.favorite_communities.all()

    def get_administrated_communities(self):
        return Community.objects.filter(memberships__user=self, memberships__is_administrator=True)

    def get_moderated_communities(self):
        return Community.objects.filter(memberships__user=self, memberships__is_moderator=True)


        '''''проги для подписчиков  60-109'''''

    def follow_user(self, user):
        return self.follow_user_with_id(user.pk)

    def follow_user_with_id(self, user_id):
        check_can_follow_user_with_id(user_id=user_id, user=self)
        if self.pk == user_id:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        follow = Follow.create_follow(user_id=self.pk, followed_user_id=user_id)
        return follow

    def community_follow_user(self, community_name):
        return self.follow_community_with_name(community_name)

    def follow_community_with_name(self, community_name):
        check_can_join_community_with_name(
            user=self,
            community_name=community_name)
        follow = CommunityFollow.create_follow(user_id=self.pk, community_name=community_name)
        return follow

    def community_unfollow_user(self, community_name):
        return self.unfollow_community_with_name(community_name)

    def unfollow_community_with_name(self, community_name):
        check_can_join_community_with_name(user=self, community_name=community_name)
        follow = CommunityFollow.objects.get(user=self,community=community_name)
        follow.delete()

    def frend_user(self, user):
        return self.frend_user_with_id(user.pk)

    def frend_user_with_id(self, user_id):
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
        check_not_can_follow_user_with_id(user=self, user_id=user_id)
        follow = Follow.objects.get(user=self,followed_user=user_id)
        follow.delete()

    def unfrend_user(self, user):
        return self.unfrend_user_with_id(user.pk)

    def unfrend_user_with_id(self, user_id):
        check_is_following_user_with_id(user=self, user_id=user_id)
        follow = Follow.create_follow(user_id=user_id, followed_user_id=self.pk)
        connection = self.connections.get(target_connection__user_id=user_id)
        connection.delete()

    def unblock_user_with_username(self, username):
        user = User.objects.get(username=username)
        return self.unblock_user_with_id(user_id=user.pk)

    def unblock_user_with_id(self, user_id):
        check_can_unblock_user_with_id(user=self, user_id=user_id)
        self.user_blocks.filter(blocked_user_id=user_id).delete()
        return User.objects.get(pk=user_id)

    def block_user_with_username(self, username):
        user = User.objects.get(username=username)
        return self.block_user_with_id(user_id=user.pk)

    def block_user_with_id(self, user_id):
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
        return UserBlock.users_are_blocked(user_a_id=self.pk, user_b_id=user_id)

    def is_connected_with_user_with_id(self, user_id):
        return self.connections.filter(
            target_connection__user_id=user_id).exists()

    def is_connected_with_user_with_username(self, username):
        return self.connections.filter(
            target_connection__user__username=username).exists()

    def is_pending_confirm_connection_for_user_with_id(self, user_id):
        if not self.is_connected_with_user_with_id(user_id):
            return False
        connection = self.connections.filter(
            target_connection__user_id=user_id).get()
        return not connection.circles.exists()

    def is_global_moderator(self):
        moderators_community_name = settings.MODERATORS_COMMUNITY_NAME
        return self.is_member_of_community_with_name(community_name=moderators_community_name)

    def is_invited_to_community_with_name(self, community_name):
        return Community.is_user_with_username_invited_to_community_with_name(username=self.username,
                                                                              community_name=community_name)

    def is_administrator_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_administrator=True).exists()

    def is_staff_of_community_with_name(self, community_name):
        return self.is_administrator_of_community_with_name(
            community_name=community_name) or self.is_moderator_of_community_with_name(community_name=community_name)

    def is_member_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name).exists()

    def is_banned_from_community_with_name(self, community_name):
        return self.banned_of_communities.filter(name=community_name).exists()

    def is_closed_profile(self):
        try:
            user_private = UserPrivateSettings.objects.get(user=self)
            return user_private.is_private
        except:
            user_private = UserPrivateSettings.objects.create(user=self)
            return False

    def is_creator_of_community_with_name(self, community_name):
        return self.created_communities.filter(name=community_name).exists()

    def is_moderator_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_moderator=True).exists()

    def is_following_user_with_id(self, user_id):
        return self.follows.filter(followed_user__id=user_id).exists()

    def is_following_user_with_username(self, user_username):
        return self.follows.filter(followed_user__username=user_username).exists()

    def is_suspended(self):
        return self.moderation_penalties.filter(type=ModerationPenalty.TYPE_SUSPENSION,
                                                expiration__gt=timezone.now()).exists()

    def is_administrator_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_administrator=True).exists()

    def is_staff_of_community_with_name(self, community_name):
        return self.is_administrator_of_community_with_name(
            community_name=community_name) or self.is_moderator_of_community_with_name(community_name=community_name)


    ''''' количества всякие  196-216 '''''


    def count_followers(self):
        return Follow.objects.filter(followed_user__id=self.pk).count()

    def count_following(self):
        return self.followers.count()

    def count_connections(self):
        return self.connections.count()

    def count_community(self):
        return self.communities_memberships.count()

    def count_photos(self):
        return self.photo_creator.count()

    def count_albums(self):
        return self.created_user.count()

    def count_goods(self):
        goods = Good.objects.filter(creator__id=self.pk,is_deleted=False).count()
        return goods

    def count_posts(self):
        return self.posts.count()


    ''''' GET всякие  219-186 '''''
    def get_pop_connection(self):
        connection_query = Q(target_connection__user_id=self.id)
        exclude_reported_and_approved_posts_query = ~Q(target_connection__user__moderated_object__status=ModeratedObject.STATUS_APPROVED)
        connection_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        connection_query.add(~Q(Q(target_connection__user__blocked_by_users__blocker_id=self.pk) | Q(target_connection__user__user_blocks__blocked_user_id=self.pk)), Q.AND)
        connection = Connect.objects.filter(connection_query)
        return connection[0:5]

    def get_all_connection(self):
        connection_query = Q(target_connection__user_id=self.id)
        exclude_reported_and_approved_posts_query = ~Q(target_connection__user__moderated_object__status=ModeratedObject.STATUS_APPROVED)
        connection_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        connection_query.add(~Q(Q(target_connection__user__blocked_by_users__blocker_id=self.pk) | Q(target_connection__user__user_blocks__blocked_user_id=self.pk)), Q.AND)
        connection = Connect.objects.filter(connection_query)
        return connection

    def get_common_friend(self):
        my_connections = self.get_all_connection()
        query = ""
        for frend in my_connections:
            user_id = frend.user.pk
            if user_id != self.pk:
                list = frend.user.get_all_connection()
                query = query + str(list)
        return query


    def get_online_connection(self):
        online_connection = self.get_all_connection().get_online()
        return online_connection


    def get_posts(self):
        posts_query = Q(creator_id=self.id, is_deleted=False, status=Item.STATUS_PUBLISHED, community=None)
        exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        posts_query.add(exclude_reported_and_approved_posts_query, Q.AND)
        items = Item.objects.filter(posts_query)
        return items

    def get_photos(self):
        photos_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community=None)
        exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos

    def get_avatar_photos(self):
        photos_query = Q(creator_id=self.id, is_deleted=False, community=None, album_2__title="Фото со страницы", album_2__is_generic=True)
        exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        avatar_photos = Photo.objects.filter(photos_query)
        return avatar_photos

    def get_albums(self):
        albums_query = Q(creator_id=self.id, is_deleted=False, is_public=True, community=None)
        exclude_reported_and_approved_albums_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        albums_query.add(exclude_reported_and_approved_albums_query, Q.AND)
        albums = Album.objects.filter(albums_query)
        return albums

    def get_goods(self):
        goods_query = Q(creator_id=self.id, is_deleted=False, status=Good.STATUS_PUBLISHED)
        exclude_reported_and_approved_goods_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        goods_query.add(exclude_reported_and_approved_goods_query, Q.AND)
        goods = Good.objects.filter(goods_query)
        return goods

    def get_avatar(self):
        try:
            avatar = self.get_avatar_photos().order_by('-id')[0]
        except:
            avatar = None
        return avatar

    def get_followers(self):
        followers_query = self._make_followers_query()
        return User.objects.filter(followers_query).distinct()

    def get_followings(self):
        followings_query = self._make_followings_query()
        return User.objects.filter(followings_query).distinct()

    def get_timeline_posts(self):
        return self._get_timeline_posts_with_no_filters()

    def _get_timeline_posts_with_no_filters(self):
        posts_select_related = ('creator', 'creator__profile', 'community')
        items_only = ('id', 'uuid', 'created', 'creator__username', 'creator__id',
                        'creator__profile__id', 'community__id', 'community__name')
        reported_posts_exclusion_query = ~Q(moderated_object__reports__reporter_id=self.pk)
        own_posts_query = Q(creator=self.pk, community__isnull=True, is_deleted=False, status=Item.STATUS_PUBLISHED)
        own_posts_query.add(reported_posts_exclusion_query, Q.AND)
        own_posts_queryset = self.items.select_related(*posts_select_related).only(*items_only).filter(own_posts_query)

        community_posts_query = Q(community__memberships__user__id=self.pk, is_closed=False, is_deleted=False, status=Item.STATUS_PUBLISHED)
        community_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(creator__user_blocks__blocked_user_id=self.pk)), Q.AND)
        community_posts_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
        community_posts_query.add(reported_posts_exclusion_query, Q.AND)
        community_posts_queryset = Item.objects.select_related(*posts_select_related).only(*items_only).filter(community_posts_query)

        followed_users = self.follows.values('followed_user_id')
        followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
        followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, status=Item.STATUS_PUBLISHED)
        followed_users_query.add(reported_posts_exclusion_query, Q.AND)
        followed_users_queryset = Item.objects.select_related(*posts_select_related).only(*items_only).filter(followed_users_query)

        frends = self.connections.values('target_user_id')
        frends_ids = [target_user['target_user_id'] for target_user in frends]
        frends_query = Q(creator__in=frends_ids, is_deleted=False, status=Item.STATUS_PUBLISHED)
        frends_query.add(reported_posts_exclusion_query, Q.AND)
        frends_queryset = Item.objects.select_related(*posts_select_related).only(*items_only).filter(frends_query)
        final_queryset = own_posts_queryset.union(community_posts_queryset, followed_users_queryset, frends_queryset)

        return final_queryset

    def join_community_with_name(self, community_name):
        check_can_join_community_with_name(user=self, community_name=community_name)
        community_to_join = Community.objects.get(name=community_name)
        community_to_join.add_member(self)
        if community_to_join.is_private():
            CommunityInvite.objects.filter(community_name=community_name, invited_user__id=self.id).delete()
        if community_to_join.is_closed():
            CommunityFollow.objects.filter(community_name=community_name, community_follows__id=self.id).delete()
        return community_to_join

    def leave_community_with_name(self, community_name):
        check_can_leave_community_with_name(
            user=self,
            community_name=community_name)
        community_to_leave = Community.objects.get(name=community_name)
        if self.has_favorite_community_with_name(community_name):
            self.unfavorite_community_with_name(community_name=community_name)
        community_to_leave.remove_member(self)
        return community_to_leave

    def _make_get_votes_query(self, item):
        reactions_query = Q(parent_id=item.pk)
        post_community = item.community

        if post_community:
            if not self.is_staff_of_community_with_name(community_name=post_community.name):
                blocked_users_query = ~Q(Q(user__blocked_by_users__blocker_id=self.pk) | Q(user__user_blocks__blocked_user_id=self.pk))
                blocked_users_query_staff_members = Q(user__communities_memberships__community_id=post_community.pk)
                blocked_users_query_staff_members.add(Q(user__communities_memberships__is_administrator=True) | Q(user__communities_memberships__is_moderator=True), Q.AND)
                blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
                reactions_query.add(blocked_users_query, Q.AND)
        else:
            blocked_users_query = ~Q(Q(user__blocked_by_users__blocker_id=self.pk) | Q(user__user_blocks__blocked_user_id=self.pk))
            reactions_query.add(blocked_users_query, Q.AND)
        return reactions_query

    def _make_get_votes_query_comment(self, comment):
        reactions_query = Q(item_id=comment.pk)
        try:
            post_community = comment.item.community
        except:
            post_community = comment.parent_comment.item.community

        if post_community:
            if not self.is_staff_of_community_with_name(community_name=post_community.name):
                blocked_users_query = ~Q(Q(user__blocked_by_users__blocker_id=self.pk) | Q(user__user_blocks__blocked_user_id=self.pk))
                blocked_users_query_staff_members = Q(user__communities_memberships__community_id=post_community.pk)
                blocked_users_query_staff_members.add(Q(user__communities_memberships__is_administrator=True) | Q(user__communities_memberships__is_moderator=True), Q.AND)
                blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
                reactions_query.add(blocked_users_query, Q.AND)
        else:
            blocked_users_query = ~Q(Q(user__blocked_by_users__blocker_id=self.pk) | Q(user__user_blocks__blocked_user_id=self.pk))
            reactions_query.add(blocked_users_query, Q.AND)
        return reactions_query

    def has_favorite_community_with_name(self, community_name):
        return self.favorite_communities.filter(name=community_name).exists()

    def has_excluded_community_with_name(self, community_name):
        return self.top_posts_community_exclusions.filter(community__name=community_name).exists()

    def has_blocked_user_with_id(self, user_id):
        return self.user_blocks.filter(blocked_user_id=user_id).exists()


class UserBlock(models.Model):
    blocked_user = models.ForeignKey(User, db_index=False, on_delete=models.CASCADE, related_name='blocked_by_users', verbose_name="Кого блокирует")
    blocker = models.ForeignKey(User, db_index=False, on_delete=models.CASCADE, related_name='user_blocks', verbose_name="Кто блокирует")

    @classmethod
    def create_user_block(cls, blocker_id, blocked_user_id):
        return cls.objects.create(blocker_id=blocker_id, blocked_user_id=blocked_user_id)

    @classmethod
    def users_are_blocked(cls, user_a_id, user_b_id):
        return cls.objects.filter(Q(blocked_user_id=user_a_id, blocker_id=user_b_id) | Q(blocked_user_id=user_b_id,
                                                                                         blocker_id=user_a_id)).exists()

    class Meta:
        unique_together = ('blocked_user', 'blocker',)
        indexes = [
            models.Index(fields=['blocked_user', 'blocker']),
        ]


class UserNotificationsSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications_settings', verbose_name="Пользователь")
    comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к записям")
    react_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о реакциях к записи")
    comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к записям")
    comment_reply_react_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления реакциях на ответы к комментариям")
    comment_react_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о реакциях на комментарии к записям")
    connection_request_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о заявках в друзья")
    connection_confirmed_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о приеме заявки в друзья")
    community_invite_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о приглашениях в сообщества")
    comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к записям")
    user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в записям")
    repost_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о репостах записей")

    @classmethod
    def create_notifications_settings(cls, user):
        return UserNotificationsSettings.objects.create(user=user)


class UserPrivateSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_private", on_delete=models.CASCADE, verbose_name="Пользователь")
    is_private = models.BooleanField(default=False, verbose_name="Закрытый профиль")
    can_message = models.BooleanField(default=True, verbose_name="Вам могут писать сообщения все пользователи")
    photo_visible_all = models.BooleanField(default=True, verbose_name="Ваши фото видны всем")
    photo_visible_frends = models.BooleanField(default=True, verbose_name="Ваши фото видны Вашим друзьям")
    can_comments = models.BooleanField(default=True, verbose_name="Могут оставлять комментарии все пользователи")
    can_add_post = models.BooleanField(default=False, verbose_name="Вам могут писать записи на стене")
    can_add_article = models.BooleanField(default=False, verbose_name="Вам могут писать статьи на стене")
    can_add_good = models.BooleanField(default=False, verbose_name="Вам могут добавлять товары")

    @classmethod
    def create_private_settings(cls, user):
        return UserPrivateSettings.objects.create(user=user)


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, db_index=False)
    user = models.OneToOneField(User, db_index=False, related_name="profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    cover = models.ImageField(blank=True, null=True, upload_to="users", verbose_name="Фон")
    bio = models.TextField(max_length=settings.PROFILE_BIO_MAX_LENGTH, blank=True, verbose_name="Биография")
    followers_count_visible = models.BooleanField(blank=False, null=False, default=False, verbose_name="Число подписчиков видно")
    sity = models.CharField(max_length=settings.PROFILE_LOCATION_MAX_LENGTH, blank=True, verbose_name="Местоположение")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    vk_url = models.URLField(blank=True, verbose_name="Ссылка на vk")
    youtube_url = models.URLField(blank=True, verbose_name="Ссылка на youtube")
    facebook_url = models.URLField(blank=True, verbose_name="Ссылка на facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Ссылка на instagram")
    twitter_url = models.URLField(blank=True, verbose_name="Ссылка на twitter")
    phone = models.CharField(max_length=15,blank=True, verbose_name="Телефон")
    is_global_moderator = models.BooleanField(blank=False, null=False, default=False, verbose_name="Глобальный модератор")
    is_superuser = models.BooleanField(blank=False, null=False, default=False, verbose_name="Суперпользователь")

    def __str__(self):
        return self.user.last_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

        index_together = [
            ('id', 'user'),
        ]


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='bootstrap_notifications_settings')
def create_user_notifications_settings(sender, instance=None, created=False, **kwargs):
    """"
    Create a user notifications settings for users
    """
    if created:
        bootstrap_user_notifications_settings(instance)

def bootstrap_user_notifications_settings(user):
    return UserNotificationsSettings.create_notifications_settings(user=user)
