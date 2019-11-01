from datetime import datetime, timedelta
import uuid
from django.utils import six, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from users.helpers import upload_to_user_cover_directory, upload_to_user_avatar_directory
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community
from follows.models import Follow
from goods.models import Good
from frends.models import Connect
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
        check_can_follow_user_with_id(user=self, user_id=user_id)
        if self.pk == user_id:
            raise ValidationError('Вы не можете подписаться сами на себя',)
        follow = Follow.create_follow(user_id=self.pk, followed_user_id=user_id)
        return follow

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
        check_can_follow_user_with_id(user=self, user_id=user_id)
        follow = Follow.create_follow(user_id=user_id)
        follow.delete()

    def unfrend_user(self, user):
        return self.unfrend_user_with_id(user.pk)

    def unfrend_user_with_id(self, user_id):
        check_is_following_user_with_id(user=self, user_id=user_id)
        follow = follow_user(self, user_id)
        connection = self.connections.get(target_connection__user_id=user_id)
        connection.delete()

    def get_followers(self, max_id=None):
        followers_query = self._make_followers_query()
        if max_id:
            followers_query.add(Q(id__lt=max_id), Q.AND)
        return User.objects.filter(followers_query).distinct()

    def get_followings(self, max_id=None):
        followings_query = self._make_followings_query()
        if max_id:
            followings_query.add(Q(id__lt=max_id), Q.AND)
        return User.objects.filter(followings_query).distinct()

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

    def is_member_of_communities(self):
        return self.communities_memberships.all().exists()

    def is_member_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name).exists()

    def is_banned_from_community_with_name(self, community_name):
        return self.banned_of_communities.filter(name=community_name).exists()

    def is_creator_of_community_with_name(self, community_name):
        return self.created_communities.filter(name=community_name).exists()

    def is_moderator_of_community_with_name(self, community_name):
        return self.communities_memberships.filter(community__name=community_name, is_moderator=True).exists()

    def is_following_user_with_id(self, user_id):
        return self.follows.filter(followed_user__id=user_id).exists()

    def is_following_user_with_username(self, user_username):
        return self.follows.filter(followed_user__username=user_username).exists()


    ''''' количества всякие  196-216 '''''


    def count_followers(self):
        return Follow.objects.filter(followed_user__id=self.pk).count()

    def count_following(self):
        return self.followers.count()

    def count_connections(self):
        return self.connections.count()

    def count_community(self):
        return self.memberships__user__id.count()

    def count_goods(self):
        goods = Good.objects.filter(creator__id=self.pk,is_deleted=False).count()
        return goods

    def count_posts(self):
        return self.posts.count()


    ''''' GET всякие  219-186 '''''
    def get_pop_connection(self):
        connection = Connect.objects.filter(target_connection__user_id=self.id)
        return connection[0:5]

    def get_all_connection(self):
        connection = Connect.objects.filter(target_connection__user_id=self.id)
        return connection




class UserBlock(models.Model):
    blocked_user = models.ForeignKey(User, db_index=False, on_delete=models.CASCADE, related_name='blocked_by_users')
    blocker = models.ForeignKey(User, db_index=False, on_delete=models.CASCADE, related_name='user_blocks')

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='notifications_settings', verbose_name="Пользователь")
    post_comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к постам")
    post_comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к постам")
    follow_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о подписках")
    connection_request_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о заявках в друзья")
    connection_confirmed_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о приеме заявки в друзья")
    community_invite_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о приглашениях в сообщества")
    post_comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к постам")
    post_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в постам")

    @classmethod
    def create_notifications_settings(cls, user):
        return UserNotificationsSettings.objects.create(user=user)

    def update(self, post_comment_notifications=None,
               post_comment_reply_notifications=None,
               follow_notifications=None,
               connection_request_notifications=None,
               connection_confirmed_notifications=None,
               community_invite_notifications=None,
               post_comment_user_mention_notifications=None,
               post_user_mention_notifications=None, ):

        if post_comment_notifications is not None:
            self.post_comment_notifications = post_comment_notifications

        if post_comment_user_mention_notifications is not None:
            self.post_comment_user_mention_notifications = post_comment_user_mention_notifications

        if post_user_mention_notifications is not None:
            self.post_user_mention_notifications = post_user_mention_notifications

        if post_comment_reply_notifications is not None:
            self.post_comment_reply_notifications = post_comment_reply_notifications

        if follow_notifications is not None:
            self.follow_notifications = follow_notifications

        if connection_request_notifications is not None:
            self.connection_request_notifications = connection_request_notifications

        if connection_confirmed_notifications is not None:
            self.connection_confirmed_notifications = connection_confirmed_notifications

        if community_invite_notifications is not None:
            self.community_invite_notifications = community_invite_notifications

        self.save()


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, db_index=False)
    user = models.OneToOneField(User, db_index=False, null=True, related_name="profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    avatar = ProcessedImageField(verbose_name='Аватар', blank=False, null=True, format='JPEG',
                                 options={'quality': 90}, processors=[ResizeToFill(500, 500)],
                                 upload_to=upload_to_user_avatar_directory)
    cover = models.ImageField(blank=True, null=True, upload_to=upload_to_user_cover_directory, verbose_name="Фон")
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
