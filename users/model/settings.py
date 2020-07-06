from django.conf import settings
from django.db import models

class UserNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notify', verbose_name="Пользователь")
    connection_request_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о заявках в друзья")
    connection_confirmed_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о приеме заявки в друзья")
    community_invite_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о приглашениях в сообщества")


class UserItemNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_item_notify', verbose_name="Пользователь")
    comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к записям")
    comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к записям")
    comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к записям")
    user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в записям")
    repost_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о репостах записей")
    like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках к записям")
    dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках к записям")
    comment_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на комментарии к записям")
    comment_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на комментарии к записям")
    comment_reply_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на ответы к комментариям")
    comment_reply_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на ответы к комментариям")

class UserPhotoNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_photo_notify', verbose_name="Пользователь")
    comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к записям")
    comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к записям")
    comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к записям")
    user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в записям")
    repost_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о репостах записей")
    like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках к записям")
    dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках к записям")
    comment_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на комментарии к записям")
    comment_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на комментарии к записям")
    comment_reply_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на ответы к комментариям")
    comment_reply_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на ответы к комментариям")

class UserGoodNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_good_notify', verbose_name="Пользователь")
    comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к записям")
    comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к записям")
    comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к записям")
    user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в записям")
    repost_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о репостах записей")
    like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках к записям")
    dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках к записям")
    comment_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на комментарии к записям")
    comment_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на комментарии к записям")
    comment_reply_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на ответы к комментариям")
    comment_reply_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на ответы к комментариям")

class UserVideoNotifications(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_video_notify', verbose_name="Пользователь")
    comment_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о комментариях к записям")
    comment_reply_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об ответах на комментарии к записям")
    comment_user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в комментариях к записям")
    user_mention_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления об упоминаниях в записям")
    repost_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о репостах записей")
    like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках к записям")
    dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках к записям")
    comment_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на комментарии к записям")
    comment_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на комментарии к записям")
    comment_reply_like_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о лайках на ответы к комментариям")
    comment_reply_dislike_notifications = models.BooleanField(default=True, verbose_name="Отправлять уведомления о дизлайках на ответы к комментариям")


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
    can_message = models.BooleanField(default=True, verbose_name="Вам могут писать сообщения все пользователи")
    photo_visible_all = models.BooleanField(default=True, verbose_name="Ваши фото видны всем")
    photo_visible_frends = models.BooleanField(default=True, verbose_name="Ваши фото видны Вашим друзьям")
    can_comments = models.BooleanField(default=True, verbose_name="Могут оставлять комментарии все пользователи")
    can_add_post = models.BooleanField(default=False, verbose_name="Вам могут писать записи на стене")
    can_add_article = models.BooleanField(default=False, verbose_name="Вам могут писать статьи на стене")
    can_add_good = models.BooleanField(default=False, verbose_name="Вам могут добавлять товары")
