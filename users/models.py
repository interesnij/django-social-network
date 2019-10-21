from datetime import datetime, timedelta
import uuid
from django.utils import six, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from users.helpers import upload_to_user_cover_directory, upload_to_user_avatar_directory
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='users')
    is_email_verified = models.BooleanField(default=False)
    are_guidelines_accepted = models.BooleanField(default=False)
    is_deleted = models.BooleanField(
        verbose_name="Удален",
        default=False,
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="uuid")
    invite_count = models.SmallIntegerField(default=0, verbose_name="Кол-во приглашений")
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
