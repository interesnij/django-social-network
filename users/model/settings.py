from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_notify', verbose_name="Пользователь")
    connection_request = models.BooleanField(default=True, verbose_name="Заявка в друзья")
    connection_confirmed = models.BooleanField(default=True, verbose_name="Заявка принята")
    community_invite = models.BooleanField(default=True, verbose_name="Приглашение в сообщество")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserNotifications.objects.create(user=instance)

class UserNotificationsPost(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_post_notify', verbose_name="Пользователь")
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

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserNotificationsPost.objects.create(user=instance)

class UserNotificationsPhoto(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_photo_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к фото")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к фото")
    repost = models.BooleanField(default=True, verbose_name="Репост фото")
    like = models.BooleanField(default=True, verbose_name="Лайк к фото")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к фото")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к фото")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к фото")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserNotificationsPhoto.objects.create(user=instance)

class UserNotificationsGood(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_good_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к товару")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к товару")
    repost = models.BooleanField(default=True, verbose_name="Репост товара")
    like = models.BooleanField(default=True, verbose_name="Лайк к товару")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к товару")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к товару")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к товару")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserNotificationsGood.objects.create(user=instance)

class UserNotificationsVideo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_video_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к видео")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к видео")
    repost = models.BooleanField(default=True, verbose_name="Репост видео")
    like = models.BooleanField(default=True, verbose_name="Лайк к видео")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к видео")
    comment_like = models.BooleanField(default=True, verbose_name="Лайках на комментарий к видео")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к видео")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserNotificationsVideo.objects.create(user=instance)

class UserNotificationsMusic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_music_notify', verbose_name="Пользователь")
    repost = models.BooleanField(default=True, verbose_name="Репост аудиозаписи")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserNotificationsMusic.objects.create(user=instance)


class UserColorSettings(models.Model):
    COLOR = (
        ('white', 'white'),
        ('blue', 'blue'),
        ('brown', 'brown'),
        ('dark-blue', 'dark-blue'),
        ('dark-brown', 'dark-brown'),
        ('dark-green', 'dark-green'),
        ('dark-grey', 'dark-grey'),
        ('dark-maroon', 'dark-maroon'),
        ('dark-pink', 'dark-pink'),
        ('dark-purple', 'dark-purple'),
        ('grey', 'grey'),
        ('orange', 'orange'),
        ('purple', 'purple'),
        ('red', 'red'),
        ('skyblue', 'skyblue'),
        ('teal', 'teal'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='color_settings', verbose_name="Пользователь")
    color = models.CharField(max_length=20, choices=COLOR, default='white', verbose_name="Цвет")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserColorSettings.objects.create(user=instance)

class ProfilePrivate(models.Model):
    ALL_CAN, MEMBERS, FRIENDS_MEMBERS, FRIENDS, EACH_OTHER, YOU, FRIENDS_BUT, SOME_FRIENDS, MEMBERS_BUT, SOME_MEMBERS = 1,2,3,4,5,6,17,18,19,20
    PERM = ((ALL_CAN, 'Все пользователи'),(FRIENDS, 'Друзья'),(EACH_OTHER, 'Друзья и друзья друзей'),(YOU, 'Только я'),(FRIENDS_BUT, 'Друзья, кроме'),(SOME_FRIENDS, 'Некоторые друзья'),)
    PERM_PLANNER = (
        (ALL_CAN, 'Все пользователи'),
        (MEMBERS, 'Участники пространства или доски'),
        (FRIENDS, 'Друзья'),
        (FRIENDS_MEMBERS, 'Друзья и участники'),
        (EACH_OTHER, 'Друзья и друзья друзей'),
        (YOU, 'Только я'),
        (FRIENDS_BUT, 'Друзья, кроме'),
        (SOME_FRIENDS, 'Некоторые друзья'),
        (MEMBERS_BUT, 'Участники, кроме'),
        (SOME_MEMBERS, 'Некоторые участники'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='profile_private', verbose_name="Пользователь")
    can_see_community = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит сообщества")
    can_see_info = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит информацию")
    can_see_friend = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит друзей")
    can_send_message = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет сообщения")
    can_add_in_chat = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто добавляет в беседы")
    can_see_post = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит стену")
    can_see_photo = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет сообщения")
    can_see_good = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет сообщения")
    can_see_video = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет сообщения")
    can_see_music = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет сообщения")
    can_see_planner = models.PositiveSmallIntegerField(choices=PERM_PLANNER, default=2, verbose_name="Кто видит раздел планирования")
    can_see_doc = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит документы")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ProfilePrivate.objects.create(user=instance)
