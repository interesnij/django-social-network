from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from users.models import User


class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',verbose_name="Владелец")
    created = models.DateTimeField(editable=False, db_index=True,verbose_name="Создано")
    read = models.BooleanField(default=False,verbose_name="Прочитано")

    POST_REACTION = 'PR'
    POST_COMMENT = 'PC'
    POST_COMMENT_REPLY = 'PCR'
    POST_COMMENT_REACTION = 'PCRA'
    CONNECTION_REQUEST = 'CR'
    CONNECTION_CONFIRMED = 'CC'
    FOLLOW = 'F'
    COMMUNITY_INVITE = 'CI'
    POST_USER_MENTION = 'PUM'
    POST_COMMENT_USER_MENTION = 'PCUM'

    NOTIFICATION_TYPES = (
        (POST_REACTION, 'Рекция на пост'),
        (POST_COMMENT, 'Комментарий к посту'),
        (POST_COMMENT_REPLY, 'Ответ на комментарий к посту'),
        (POST_COMMENT_REACTION, 'Рефкция на комментарий к посту'),
        (CONNECTION_REQUEST, 'Заявка в друзья'),
        (CONNECTION_CONFIRMED, 'Одобренная заявка в друзья'),
        (FOLLOW, 'Подписка'),
        (COMMUNITY_INVITE, 'Приглашение в сообщество'),
        (POST_USER_MENTION, 'Упоминание пользователя в посте'),
        (POST_COMMENT_USER_MENTION, 'Упоминание пользователя в комментарии к посту'),
    )

    notification_type = models.CharField(max_length=5, choices=NOTIFICATION_TYPES,verbose_name="Тип уведомления")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
