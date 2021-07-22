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


class UserPrivate(models.Model):
    ALL_CAN, FRIENDS, MEMBERS, FRIENDS_MEMBERS, EACH_OTHER, YOU, FRIENDS_BUT, MEMBERS_BUT, SOME_FRIENDS, SOME_MEMBERS = 'AC','F','M','FM','EO','Y','FB','MB','SF','SM'
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private', verbose_name="Пользователь")
    can_see_community = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто видит сообщества")
    can_see_friend = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто видит друзей")
    can_receive_message = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет сообщения")
    can_see_post = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто видит стену")
    can_see_photo = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет сообщения")
    can_see_good = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет сообщения")
    can_see_video = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет сообщения")
    can_see_music = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет сообщения")
    can_see_planner_workspace = models.CharField(max_length=2, choices=PERM_PLANNER, default=MEMBERS, verbose_name="Кто видит рабочие пространства и весь раздел планирования")
    can_see_planner_board = models.CharField(max_length=2, choices=PERM_PLANNER, default=MEMBERS, verbose_name="Кто видит доски планирования")
    can_see_planner_column = models.CharField(max_length=2, choices=PERM_PLANNER, default=MEMBERS, verbose_name="Кто видит колонки досок планирования")
    can_see_doc = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто видит документы")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivate.objects.create(user=instance)

class UserPrivatePost(models.Model):
    ALL_CAN, FRIENDS, EACH_OTHER, YOU, FRIENDS_BUT, SOME_FRIENDS = 'AC','F','EO','Y','AB','SF'
    PERM = ((ALL_CAN, 'Все пользователи'),(FRIENDS, 'Друзья'),(EACH_OTHER, 'Друзья и друзья друзей'),(YOU, 'Только я'),(FRIENDS_BUT, 'Друзья, кроме'),(SOME_FRIENDS, 'Некоторые друзья'),)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private_post', verbose_name="Пользователь")
    can_see_comment = models.CharField(max_length=5, choices=PERM, default=ALL_CAN, verbose_name="Кто видит комментарии")
    vote_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    add_item = models.CharField(max_length=5, choices=PERM, default=YOU, verbose_name="Кто добавляет записи и потом с этими записями работает")
    add_comment = models.CharField(max_length=5, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет комментарии")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivatePost.objects.create(user=instance)

class UserPrivatePhoto(models.Model):
    ALL_CAN, FRIENDS, EACH_OTHER, YOU, FRIENDS_BUT, SOME_FRIENDS = 'AC','F','EO','Y','AB','SF'
    PERM = ((ALL_CAN, 'Все пользователи'),(FRIENDS, 'Друзья'),(EACH_OTHER, 'Друзья и друзья друзей'),(YOU, 'Только я'),(FRIENDS_BUT, 'Друзья, кроме'),(SOME_FRIENDS, 'Некоторые друзья'),)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private_photo', verbose_name="Пользователь")
    can_see_comment = models.CharField(max_length=5, choices=PERM, default=ALL_CAN, verbose_name="Кто видит комментарии")
    vote_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    add_item = models.CharField(max_length=5, choices=PERM, default=YOU, verbose_name="Кто добавляет фотографии и потом с этими фотографями работает")
    add_comment = models.CharField(max_length=5, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет комментарии")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivatePhoto.objects.create(user=instance)

class UserPrivateGood(models.Model):
    ALL_CAN, FRIENDS, EACH_OTHER, YOU, FRIENDS_BUT, SOME_FRIENDS = 'AC','F','EO','Y','AB','SF'
    PERM = ((ALL_CAN, 'Все пользователи'),(FRIENDS, 'Друзья'),(EACH_OTHER, 'Друзья и друзья друзей'),(YOU, 'Только я'),(FRIENDS_BUT, 'Друзья, кроме'),(SOME_FRIENDS, 'Некоторые друзья'),)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private_good', verbose_name="Пользователь")
    can_see_comment = models.CharField(max_length=5, choices=PERM, default=ALL_CAN, verbose_name="Кто видит комментарии")
    vote_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    add_item = models.CharField(max_length=2, choices=PERM, default=YOU, verbose_name="Кто добавляет товары и потом с этими товарами работает")
    add_comment = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет комментарии")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivateGood.objects.create(user=instance)

class UserPrivateVideo(models.Model):
    ALL_CAN, FRIENDS, EACH_OTHER, YOU, FRIENDS_BUT, SOME_FRIENDS = 'AC','F','EO','Y','AB','SF'
    PERM = ((ALL_CAN, 'Все пользователи'),(FRIENDS, 'Друзья'),(EACH_OTHER, 'Друзья и друзья друзей'),(YOU, 'Только я'),(FRIENDS_BUT, 'Друзья, кроме'),(SOME_FRIENDS, 'Некоторые друзья'),)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private_video', verbose_name="Пользователь")
    can_see_comment = models.CharField(max_length=5, choices=PERM, default=ALL_CAN, verbose_name="Кто видит комментарии")
    vote_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    add_item = models.CharField(max_length=2, choices=PERM, default=YOU, verbose_name="Кто добавляет ролики и потом с этими роликами работает")
    add_comment = models.CharField(max_length=2, choices=PERM, default=ALL_CAN, verbose_name="Кто пишет комментарии")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivateVideo.objects.create(user=instance)


class UserPrivateMusic(models.Model):
    ALL_CAN, FRIENDS, EACH_OTHER, YOU, FRIENDS_BUT, SOME_FRIENDS = 'AC','F','EO','Y','AB','SF'
    PERM = ((ALL_CAN, 'Все пользователи'),(FRIENDS, 'Друзья'),(EACH_OTHER, 'Друзья и друзья друзей'),(YOU, 'Только я'),(FRIENDS_BUT, 'Друзья, кроме'),(SOME_FRIENDS, 'Некоторые друзья'),)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private_music', verbose_name="Пользователь")
    add_item = models.CharField(max_length=2, choices=PERM, default=YOU, verbose_name="Кто добавляет записи и потом с этими аудиозаписями работает")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivateMusic.objects.create(user=instance)

class UserPrivatePlanner(models.Model):
    ALL_CAN,FRIENDS,MEMBERS,FRIENDS_MEMBERS,EACH_OTHER,YOU,FRIENDS_BUT,MEMBERS_BUT,SOME_FRIENDS,SOME_MEMBERS = 'AC','F','M','FM','EO','Y','FB','MB','SF','SM'
    PERM = (
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='user_private_planner', verbose_name="Пользователь")
    can_see_comments = models.CharField(max_length=2, choices=PERM, default=MEMBERS, verbose_name="Кто видит комментарии")
    add_comments = models.CharField(max_length=2, choices=PERM, default=MEMBERS, verbose_name="Кто добавляет комментарии")
    vote_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserPrivatePlanner.objects.create(user=instance)
