from datetime import datetime, timedelta
import uuid
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils import six, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from django.conf import settings

from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill, ResizeToFit



class User(AbstractUser):
    
    email = models.EmailField(unique=True, null=False, blank=False,verbose_name="Емаил")
    connections_circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE, related_name='+',null=True, blank=True)

    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
    is_email_verified = models.BooleanField(default=False)
    are_guidelines_accepted = models.BooleanField(default=False)
    # Это происходит только в том случае, если пользователь был обнаружен с критическим содержанием серьезности и его учетная запись удалена
    is_deleted = models.BooleanField(
        verbose_name="Удален",
        default=False,
    )

    username = models.CharField(
        blank=False,
        null=False,
        max_length=35,
        unique=True,
        verbose_name="Логин",
        error_messages={
            'unique': "Пользователь с таким именем пользователя уже существует.",
        },
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,verbose_name="uuid")
    invite_count = models.SmallIntegerField(default=0,verbose_name="Кол-во приглашений")

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.last_name


class UserBlock(models.Model):
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by_users')
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blocks')


class UserNotificationsSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='notifications_settings',verbose_name="Пользователь")
    post_comment_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о комментариях к постам")
    post_comment_reply_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления об ответах на комментарии к постам")
    post_reaction_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о реакциях к постам")
    follow_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о подписках")
    connection_request_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о заявках в друзья")
    connection_confirmed_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о приеме заявки в друзья")
    community_invite_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о приглашениях в сообщества")
    post_comment_reaction_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления о реакциях на комментарии к постам")
    post_comment_user_mention_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления об упоминаниях в комментариях к постам")
    post_user_mention_notifications = models.BooleanField(default=True,verbose_name="Отправлять уведомления об упоминаниях в постам")
