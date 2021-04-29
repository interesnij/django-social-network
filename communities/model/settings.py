from django.conf import settings
from django.db import models
from communities.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver
from pilkit.processors import ResizeToFill, ResizeToFit
from communities.helpers import upload_to_community_avatar_directory, upload_to_community_cover_directory
from imagekit.models import ProcessedImageField
from django.conf import settings


class CommunityInfo(models.Model):
    community = models.OneToOneField(Community, primary_key=True, related_name="community_info", verbose_name="Сообщество", on_delete=models.CASCADE)
    description = models.TextField(max_length=settings.COMMUNITY_DESCRIPTION_MAX_LENGTH, blank=True, null=True, verbose_name="Описание" )
    cover = ProcessedImageField(blank=True, format='JPEG',options={'quality': 90},upload_to=upload_to_community_avatar_directory,processors=[ResizeToFit(width=1024, upscale=False)])
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_community_cover_directory)

    posts = models.PositiveIntegerField(default=0, verbose_name="Кол-во постов")
    views_post = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров постов")
    members = models.PositiveIntegerField(default=0, verbose_name="Кол-во участников")
    photos = models.PositiveIntegerField(default=0, verbose_name="Кол-во фотографий")
    goods = models.PositiveIntegerField(default=0, verbose_name="Кол-во товаров")
    traks = models.PositiveIntegerField(default=0, verbose_name="Кол-во аудиозаписей")
    videos = models.PositiveIntegerField(default=0, verbose_name="Кол-во видеозаписей")

    def __str__(self):
        return self.user.last_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        index_together = [('id', 'user'),]

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class CommunityNotificationsPost(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_notifications_post', verbose_name="Сообщество")
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

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsPost.objects.create(community=instance)

class CommunityNotificationsPhoto(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_notifications_photo', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к фото")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к фото")
    repost = models.BooleanField(default=True, verbose_name="Репост фото")
    like = models.BooleanField(default=True, verbose_name="Лайк к фото")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к фото")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к фото")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к фото")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к фото")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к фото")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsPhoto.objects.create(community=instance)

class CommunityNotificationsGood(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_notifications_good', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к товару")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к товару")
    repost = models.BooleanField(default=True, verbose_name="Репост товара")
    like = models.BooleanField(default=True, verbose_name="Лайк к товару")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к товару")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к товару")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к товару")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к товару")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к товару")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsGood.objects.create(community=instance)

class CommunityNotificationsVideo(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_notifications_video', verbose_name="Сообщество")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к ролику")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к ролику")
    repost = models.BooleanField(default=True, verbose_name="Репост ролика")
    like = models.BooleanField(default=True, verbose_name="Лайк к ролику")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к ролику")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к ролику")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к ролику")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к ролику")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к ролику")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsVideo.objects.create(community=instance)

class CommunityNotificationsMusic(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_notifications_music', verbose_name="Сообщество")
    repost = models.BooleanField(default=True, verbose_name="Репост аудиозаписи")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsMusic.objects.create(community=instance)


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
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_private_post', verbose_name="Сообщество")
    wall = models.CharField(max_length=5, choices=WALL, default=STAFF_POST, verbose_name="Стена")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityPrivatePost.objects.create(community=instance)

class CommunityPrivatePhoto(models.Model):
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
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_private_photo', verbose_name="Сообщество")
    photo = models.CharField(max_length=5, choices=PHOTO, default=PHOTO_ADMIN, verbose_name="Фотографии")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityPrivatePhoto.objects.create(community=instance)

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
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_private_good', verbose_name="Сообщество")
    good = models.CharField(max_length=5, choices=GOOD, default=GOOD_ADMIN, verbose_name="Товар")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityPrivateGood.objects.create(community=instance)

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
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_private_video', verbose_name="Сообщество")
    video = models.CharField(max_length=5, choices=VIDEO, default=VIDEO_ADMIN, verbose_name="Ролик")
    comment = models.CharField(max_length=5, choices=COMMENT, default=COMMENT_NOMEMBER, verbose_name="Комментарии")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityPrivateVideo.objects.create(community=instance)

class CommunityPrivateMusic(models.Model):

    MUSIC_ADMIN = 'VA'
    MUSIC_MEMBER = 'VM'
    MUSIC_NOMEMBER = 'VNM'
    MUSIC = (
        (MUSIC_ADMIN, 'Аудиозаписи загружает персонал'),
        (MUSIC_MEMBER, 'Аудиозаписи загружают подписчики'),
        (MUSIC_NOMEMBER, 'Аудиозаписи загружают все'),
    )
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='community_private_music', verbose_name="Сообщество")
    music = models.CharField(max_length=5, choices=MUSIC, default=MUSIC_ADMIN, verbose_name="Аудиозапись")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityPrivateMusic.objects.create(community=instance)

class CommunitySectionsOpen(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_sections_open', verbose_name="Сообщество")
    photo = models.BooleanField(default=True, verbose_name="Галерея открыта")
    good = models.BooleanField(default=True, verbose_name="Товары открыты")
    video = models.BooleanField(default=True, verbose_name="Видеоролики открыты")
    music = models.BooleanField(default=True, verbose_name="Аудиозаписи открыты")
    doc = models.BooleanField(default=True, verbose_name="Документы открыты")
    link = models.BooleanField(default=True, verbose_name="Ссылки открыты")
    article = models.BooleanField(default=True, verbose_name="Статьи открыты")
    contacts = models.BooleanField(default=True, verbose_name="Контакты открыты")
    discussion = models.BooleanField(default=True, verbose_name="Обсуждения открыты")
    members = models.BooleanField(default=True, verbose_name="Подписчики открыты")

    #@receiver(post_save, sender='communities.Сommunity')
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunitySectionsOpen.objects.create(community=instance)
