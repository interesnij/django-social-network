from django.conf import settings
from django.db import models
from communities.models import Community


class CommunityNotificationsSettings(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_notifications_settings', verbose_name="Сообщество")
    comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к записям")
    react_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о реакциях к записи")
    comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к записям")
    comment_reply_react_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления реакциях на ответы к комментариям")
    comment_react_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о реакциях на комментарии к записям")
    connection_request_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о заявках в сообщество")
    comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к записям")
    user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в записям")
    repost_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о репостах записей")


class CommunityPrivateSettings(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_settings', verbose_name="Сообщество")
    photo_visible_all = models.BooleanField(default=True, verbose_name="Фото сообщества видны всем")
    photo_visible_member = models.BooleanField(default=True, verbose_name="Фото сообщества видны подписчикам")
    can_comments = models.BooleanField(default=True, verbose_name="Все могут оставлять комментарии все пользователи")
    can_add_post = models.BooleanField(default=False, verbose_name="Все могут писать записи на стене")
    can_add_article = models.BooleanField(default=False, verbose_name="Все могут писать статьи на стене")
    can_add_good = models.BooleanField(default=False, verbose_name="Все могут добавлять товары")
