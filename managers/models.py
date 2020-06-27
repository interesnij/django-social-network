from django.db import models
from django.conf import settings


class UserStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    ADVERTISER = 'R'
    SUPPORT = 'S'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
        (ADVERTISER, 'Рекламодатель'),
        (SUPPORT, 'Поддержка'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в профиле'
        verbose_name_plural = 'Полномочия в профиле'

class CommunityStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    ADVERTISER = 'R'
    SUPPORT = 'R'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
        (ADVERTISER, 'Рекламодатель'),
        (SUPPORT, 'Поддержка'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_community_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в сообществе'
        verbose_name_plural = 'Полномочия в сообществе'

class PostUserStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в постах пользователей'
        verbose_name_plural = 'Полномочия в постах пользователей'

class GoodUserStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в товарах пользователей'
        verbose_name_plural = 'Полномочия в товарах пользователей'

class PhotoUserStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в фотографиях пользователей'
        verbose_name_plural = 'Полномочия в фотографиях пользователей'

class VideoUserStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в видеозаписях пользователей'
        verbose_name_plural = 'Полномочия в видеозаписях пользователей'

class MusicUserStaff(models.Model):
    ADMINISTRATOR = 'A'
    MODERATOR = 'M'
    EDITOR = 'E'
    LEVEL = (
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (EDITOR, 'Редактор'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='music_user_staff', verbose_name="Особый пользователь")
    level = models.CharField(max_length=5, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в аудиозаписях пользователей'
        verbose_name_plural = 'Полномочия в аудиозаписях пользователей'


class CanWorkStaffUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_user', verbose_name="Создатель персонала")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей")
    can_work_support = models.BooleanField(default=False, verbose_name="Может добавлять техподдержку")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала'
        verbose_name_plural = 'Создатели персонала'

class CanWorkStaffCommunity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_community', verbose_name="Создатель персонала")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей")
    can_work_support = models.BooleanField(default=False, verbose_name="Может добавлять техподдержку")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала сообщетсв'
        verbose_name_plural = 'Создатели персонала сообщетсв'

class CanWorkStaffPostUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_post_user', verbose_name="Создатель персонала в записях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов записей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов записей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов записей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей записей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала записей'
        verbose_name_plural = 'Создатели персонала записей'

class CanWorkStaffGoodUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_good_user', verbose_name="Создатель персонала в товарах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов товаров")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов товаров")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов товаров")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей товаров")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала товаров'
        verbose_name_plural = 'Создатели персонала товаров'

class CanWorkStaffPhotoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_photo_user', verbose_name="Создатель персонала в фотографиях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов фотографий")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов фотографий")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов фотографий")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей фотографий")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала фотографий'
        verbose_name_plural = 'Создатели персонала фотографий'

class CanWorkStaffVideoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_video_user', verbose_name="Создатель персонала в видеозаписях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов видеозаписей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов видеозаписей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов видеозаписей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей видеозаписей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала видеозаписей'
        verbose_name_plural = 'Создатели персонала видеозаписей'

class CanWorkStaffAudioUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_audio_user', verbose_name="Создатель персонала в аудиозаписях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов аудиозаписей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов аудиозаписей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов аудиозаписей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей аудиозаписей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала аудиозаписей'
        verbose_name_plural = 'Создатели персонала аудиозаписей'
