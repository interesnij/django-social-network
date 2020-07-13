from django.conf import settings
from django.db import models
from communities.models import Community


class CommunityNotificationsSettings(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_notifications_settings', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к записи")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к записи")
    mention = models.BooleanField(default=True, verbose_name="Упоминание в записи")
    comment_mention = models.BooleanField(default=True, verbose_name="Упоминание в комментарии к записи")
    repost = models.BooleanField(default=True, verbose_name="Репост записи")
    like = models.BooleanField(default=True, verbose_name="Лайк к записи")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к записи")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к записи")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к записи")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")


class CommunityPrivateSettings(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_settings', verbose_name="Сообщество")
    open_message = models.BooleanField(default=True, verbose_name="Вам могут писать сообщения все пользователи")
    open_wall = models.BooleanField(default=False, verbose_name="Подписчики могут писать на стене")
    open_photo = models.BooleanField(default=False, verbose_name="Вам могут добавлять фото")
    open_good = models.BooleanField(default=False, verbose_name="Вам могут добавлять товары")
    open_video = models.BooleanField(default=False, verbose_name="Вам могут добавлять ролики")
