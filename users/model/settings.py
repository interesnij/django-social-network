from django.conf import settings
from django.db import models

class UserNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notify', verbose_name="Пользователь")
    connection_request = models.BooleanField(default=True, verbose_name="Заявка в друзья")
    connection_confirmed = models.BooleanField(default=True, verbose_name="Заявка принята")
    community_invite = models.BooleanField(default=True, verbose_name="Приглашение в сообщество")


class UserPostNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_post_notify', verbose_name="Пользователь")
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

class UserPhotoNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_photo_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к фото")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к фото")
    repost = models.BooleanField(default=True, verbose_name="Репост фото")
    comment_mention = models.BooleanField(default=True, verbose_name="Упоминание в комментарии к записи")
    like = models.BooleanField(default=True, verbose_name="Лайк к фото")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к фото")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к фото")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к фото")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")

class UserGoodNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_good_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к товару")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к товару")
    repost = models.BooleanField(default=True, verbose_name="Репост товара")
    comment_mention = models.BooleanField(default=True, verbose_name="Упоминание в комментарии к записи")
    like = models.BooleanField(default=True, verbose_name="Лайк к товару")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к товару")
    comment_like = models.BooleanField(default=True, verbose_name="Лайк на комментарий к товару")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к товару")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")

class UserVideoNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_video_notify', verbose_name="Пользователь")
    comment = models.BooleanField(default=True, verbose_name="Комментарий к видео")
    comment_reply = models.BooleanField(default=True, verbose_name="Ответ на комментарий к видео")
    repost = models.BooleanField(default=True, verbose_name="Репост видео")
    comment_mention = models.BooleanField(default=True, verbose_name="Упоминание в комментарии к записи")
    like = models.BooleanField(default=True, verbose_name="Лайк к видео")
    dislike = models.BooleanField(default=True, verbose_name="Дизлайк к видео")
    comment_like = models.BooleanField(default=True, verbose_name="Лайках на комментарий к видео")
    comment_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на комментарий к видео")
    comment_reply_like = models.BooleanField(default=True, verbose_name="Лайк на ответ к комментарию")
    comment_reply_dislike = models.BooleanField(default=True, verbose_name="Дизлайк на ответ к комментарию")


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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='color_settings', verbose_name="Пользователь")
    color = models.CharField(max_length=20, choices=COLOR, default='white', verbose_name="Цвет")
    id = models.BigAutoField(primary_key=True)


class UserPrivate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_private", on_delete=models.CASCADE, verbose_name="Пользователь")
    is_private = models.BooleanField(default=False, verbose_name="Закрытый профиль")
    open_message = models.BooleanField(default=True, verbose_name="Вам могут писать сообщения все пользователи")
    open_wall = models.BooleanField(default=False, verbose_name="Вам могут писать записи на стене")
    open_photo = models.BooleanField(default=False, verbose_name="Вам могут писать статьи на стене")
    open_good = models.BooleanField(default=False, verbose_name="Вам могут добавлять товары")
    open_video = models.BooleanField(default=False, verbose_name="Вам могут добавлять ролики")
