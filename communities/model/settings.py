from django.conf import settings
from django.db import models
from communities.models import Community


class CommunityNotificationsPost(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_notifications_post', verbose_name="Сообщество")
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

class CommunityNotificationsPhoto(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_notifications_photo', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к фото")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к фото")
    repost = models.BooleanField(default=True, verbose_name="Репост фото")
    like = models.BooleanField(default=True, verbose_name="Лайк к фото")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к фото")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к фото")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к фото")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к фото")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к фото")

class CommunityNotificationsGood(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_notifications_good', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к товару")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к товару")
    repost = models.BooleanField(default=True, verbose_name="Репост товара")
    like = models.BooleanField(default=True, verbose_name="Лайк к товару")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к товару")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к товару")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к товару")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к товару")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к товару")

class CommunityNotificationsVideo(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_notifications_video', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к ролику")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к ролику")
    repost = models.BooleanField(default=True, verbose_name="Репост ролика")
    like = models.BooleanField(default=True, verbose_name="Лайк к ролику")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к ролику")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к ролику")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к ролику")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к ролику")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к ролику")


class CommunityPrivatePost(models.Model):
    STAFF_POST = 'SP'
    STAFF_POST__MEMBER_CAN = 'SPMC'
    STAFF_POST__ALL_CAN = 'SPAC'
    MEMBER_POST = 'MP'
    MEMBER_POST__ALL_CAN = 'MPAC'
    ALL_CAN = 'AC'

    COMMENT_ADMIN = 'CA'
    COMMENT_MEMBER = 'CM'
    COMMENT_NOMEMBER = 'CNM'
    WALL = (
        (STAFF_POST, 'Персонал пишет'),
        (STAFF_POST__MEMBER_CAN, 'Персонал пишет, подписчики предлагают'),
        (STAFF_POST__ALL_CAN, 'Персонал пишет, все предлагают'),
        (MEMBER_POST, 'Подписчики пишут'),
        (MEMBER_POST__ALL_CAN, 'Подписчики пишут, все предлагают'),
        (ALL_CAN, 'На стене пишут все'),
    )
    COMMENT = (
        (COMMENT_ADMIN, 'Комментарии пишет персонал'),
        (COMMENT_MEMBER, 'Комментарии пишут подписчики'),
        (COMMENT_NOMEMBER, 'Комментарии пишут все'),
    )
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_post', verbose_name="Сообщество")
    wall = models.CharField(max_length=5, choices=WALL, default=STAFF_POST, verbose_name="Стена")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

class CommunityPrivateGallery(models.Model):
    PHOTO_ADMIN = 'PA'
    PHOTO_MEMBER = 'PM'
    PHOTO_NOMEMBER = 'PNM'

    COMMENT_ADMIN = 'CA'
    COMMENT_MEMBER = 'CM'
    COMMENT_NOMEMBER = 'CNM'
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
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_gallery', verbose_name="Сообщество")
    photo = models.CharField(max_length=5, choices=PHOTO, default=PHOTO_ADMIN, verbose_name="Фотографии")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

class CommunityPrivateGood(models.Model):

    GOOD_ADMIN = 'GA'
    GOOD_MEMBER = 'GM'
    GOOD_NOMEMBER = 'GNM'

    COMMENT_ADMIN = 'CA'
    COMMENT_MEMBER = 'CM'
    COMMENT_NOMEMBER = 'CNM'
    GOOD = (
        (GOOD_ADMIN, 'Товары загружает персонал'),
        (GOOD_MEMBER, 'Товары загружают подписчики'),
        (GOOD_NOMEMBER, 'Товары загружают все'),
    )
    COMMENT = (
        (COMMENT_ADMIN, 'Комментарии пишет персонал'),
        (COMMENT_MEMBER, 'Комментарии пишут подписчики'),
        (COMMENT_NOMEMBER, 'Комментарии пишут все'),
    )
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_good', verbose_name="Сообщество")
    good = models.CharField(max_length=5, choices=GOOD, default=GOOD_ADMIN, verbose_name="Товар")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

class CommunityPrivateVideo(models.Model):

    VIDEO_ADMIN = 'VA'
    VIDEO_MEMBER = 'VM'
    VIDEO_NOMEMBER = 'VNM'

    COMMENT_ADMIN = 'CA'
    COMMENT_MEMBER = 'CM'
    COMMENT_NOMEMBER = 'CNM'
    VIDEO = (
        (VIDEO_ADMIN, 'Ролики загружает персонал'),
        (VIDEO_MEMBER, 'Ролики загружают подписчики'),
        (VIDEO_NOMEMBER, 'Ролики загружают все'),
    )
    COMMENT = (
        (COMMENT_ADMIN, 'Комментарии пишет персонал'),
        (COMMENT_MEMBER, 'Комментарии пишут подписчики'),
        (COMMENT_NOMEMBER, 'Комментарии пишут все'),
    )
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_video', verbose_name="Сообщество")
    video = models.CharField(max_length=5, choices=VIDEO, default=VIDEO_ADMIN, verbose_name="Ролик")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")
