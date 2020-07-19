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
    WALL_CLOSE = 'WC'
    WALL_ADMIN = 'WA'
    WALL_MEMBER = 'WM'
    WALL_NOMEMBER = 'WNM'

    PHOTO_ADMIN = 'PA'
    PHOTO_MEMBER = 'PM'
    PHOTO_NOMEMBER = 'PNM'

    COMMENT_ADMIN = 'CA'
    COMMENT_MEMBER = 'CM'
    COMMENT_NOMEMBER = 'CNM'
    WALL = (
        (WALL_CLOSE, 'Стена закрыта'),
        (WALL_ADMIN, 'На стене пишет персонал'),
        (WALL_MEMBER, 'На стене пишут подписчики'),
        (WALL_NOMEMBER, 'На стене пишут все'),
    )
    PHOTO = (
        (PHOTO_ADMIN, 'Фото загружает персонал'),
        (PHOTO_MEMBER, 'Фото загружают подписчики'),
        (PHOTO_NOMEMBER, 'Фото загружают все'),
    )
    COMMENT = (
        (COMMENT_ADMIN, 'Комментарии пишет персонал'),
        (COMMENT_MEMBER, 'Комментарии пишут подписчики'),
        (COMMENT_NOMEMBER, 'Комментарии пишут все'),
    )
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_settings', verbose_name="Сообщество")
    wall = models.CharField(max_length=5, choices=WALL, default=WALL_ADMIN, verbose_name="Стена")
    photo = models.CharField(max_length=5, choices=PHOTO, default=PHOTO_ADMIN, verbose_name="Фотографии")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")
    open_video = models.BooleanField(default=False, verbose_name="Вам могут добавлять ролики")
