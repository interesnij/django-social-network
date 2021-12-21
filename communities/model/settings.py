from django.conf import settings
from django.db import models
from communities.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class CommunityInfo(models.Model):
    community = models.OneToOneField(Community, primary_key=True, related_name="community_info", verbose_name="Сообщество", on_delete=models.CASCADE)
    banned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='banned_of_communities', verbose_name="Черный список")
    posts = models.PositiveIntegerField(default=0, verbose_name="Кол-во постов")
    views_post = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров постов")
    members = models.PositiveIntegerField(default=0, verbose_name="Кол-во участников")
    photos = models.PositiveIntegerField(default=0, verbose_name="Кол-во фотографий")
    goods = models.PositiveIntegerField(default=0, verbose_name="Кол-во товаров")
    tracks = models.PositiveIntegerField(default=0, verbose_name="Кол-во аудиозаписей")
    videos = models.PositiveIntegerField(default=0, verbose_name="Кол-во видеозаписей")
    docs = models.PositiveIntegerField(default=0, verbose_name="Кол-во документов")
    articles = models.PositiveIntegerField(default=0, verbose_name="Кол-во статей")

    def __str__(self):
        return self.community.name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        #index_together = [('id', 'user'),]

    @receiver(post_save, sender=Community)
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityInfo.objects.create(community=instance)


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

    @receiver(post_save, sender=Community)
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

    @receiver(post_save, sender=Community)
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

    @receiver(post_save, sender=Community)
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

    @receiver(post_save, sender=Community)
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsVideo.objects.create(community=instance)

class CommunityNotificationsMusic(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_notifications_music', verbose_name="Сообщество")
    repost = models.BooleanField(default=True, verbose_name="Репост аудиозаписи")

    @receiver(post_save, sender=Community)
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityNotificationsMusic.objects.create(community=instance)

class CommunityPrivate(models.Model):
    ALL_CAN,MEMBERSHIPS,CREATOR,STAFF,MEMBERSHIPS_BUT,SOME_MEMBERSHIPS = 1,2,3,4,5,6

    PERM = ((ALL_CAN, 'Все пользователи'),(MEMBERSHIPS, 'Подписчики'),(CREATOR, 'Создатель'),(MEMBERSHIPS_BUT, 'Подписчики, кроме'),(SOME_MEMBERSHIPS, 'Некоторые подписчики'),(STAFF, 'Персонал'),)

    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_private', verbose_name="Сообщество")
    can_see_member = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит друзей")
    can_see_info = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит информацию")
    can_send_message = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_post = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит стену")
    can_see_photo = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_good = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_video = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_music = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_planner = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит раздел планирования")
    can_see_doc = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит документы")

class CommunityPrivate2(models.Model):
    ALL_CAN,MEMBERSHIPS,CREATOR,STAFF,MEMBERSHIPS_BUT,SOME_MEMBERSHIPS = 1,2,3,4,5,6

    PERM = ((ALL_CAN, 'Все пользователи'),(MEMBERSHIPS, 'Подписчики'),(CREATOR, 'Создатель'),(MEMBERSHIPS_BUT, 'Подписчики, кроме'),(SOME_MEMBERSHIPS, 'Некоторые подписчики'),(STAFF, 'Персонал'),)

    community = models.OneToOneField(Community, on_delete=models.CASCADE, primary_key=True, related_name='community_private2', verbose_name="Сообщество")
    can_see_member = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит друзей")
    can_see_info = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит информацию")
    can_send_message = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_post = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит стену")
    can_see_photo = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_good = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_video = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_music = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто пишет сообщения")
    can_see_planner = models.PositiveSmallIntegerField(default=1, choices=PERM, verbose_name="Кто видит раздел планирования")
    can_see_doc = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит документы")

    @receiver(post_save, sender=Community)
    def create_model(sender, instance, created, **kwargs):
        if created:
            CommunityPrivate2.objects.create(community=instance)
