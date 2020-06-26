from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io, sys
from users.helpers import upload_to_user_directory


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    bio = models.TextField(max_length=settings.PROFILE_BIO_MAX_LENGTH, blank=True, verbose_name="Биография")
    sity = models.CharField(max_length=settings.PROFILE_LOCATION_MAX_LENGTH, blank=True, verbose_name="Местоположение")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    vk_url = models.URLField(blank=True, verbose_name="Ссылка на vk")
    youtube_url = models.URLField(blank=True, verbose_name="Ссылка на youtube")
    facebook_url = models.URLField(blank=True, verbose_name="Ссылка на facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Ссылка на instagram")
    twitter_url = models.URLField(blank=True, verbose_name="Ссылка на twitter")
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_user_directory)


    def __str__(self):
        return self.user.last_name

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def b_avatarr(self, field):
        if field:
            image = Image.open(field)
            image = image.convert('RGB')
            image = image.resize((250, 200), Image.ANTIALIAS)
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            return InMemoryUploadedFile(output, 'ImageField',field.name, 'image/jpeg', sys.getsizeof(output), None)
        else:
            return None

    def s_avatarr(self, field):
        if field:
            image = Image.open(field)
            image = image.convert('RGB')
            image = image.resize((50, 50), Image.ANTIALIAS)
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            return InMemoryUploadedFile(output, 'ImageField',field.name, 'image/jpeg', sys.getsizeof(output), None)
        else:
            return None

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        index_together = [('id', 'user'),]


class OneUserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_location", verbose_name="Пользователь", on_delete=models.CASCADE)
    city_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    city_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    city_lat = models.FloatField(blank=True, null=True, verbose_name="Ширина города")
    city_lon = models.FloatField(blank=True, null=True, verbose_name="Долгота города")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    phone = models.CharField(max_length=5, blank=True, verbose_name="Начало номера")

    class Meta:
        verbose_name="Местоположение 1"
        verbose_name_plural="Местоположения 1"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{}, {}, {}'.format(self.country_ru, self.region_ru, self.city_ru)
    def get_sity(self):
        return self.city_ru


class TwoUserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_location_2", verbose_name="Пользователь", on_delete=models.CASCADE)
    city_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    city_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    city_lat = models.FloatField(blank=True, null=True, verbose_name="Ширина города")
    city_lon = models.FloatField(blank=True, null=True, verbose_name="Долгота города")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    phone = models.CharField(max_length=5, blank=True, verbose_name="Начало номера")

    class Meta:
        verbose_name="Местоположение 2"
        verbose_name_plural="Местоположения 2"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{}, {}, {}'.format(self.country_ru, self.region_ru, self.city_ru)

class ThreeUserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_location_3", verbose_name="Пользователь", on_delete=models.CASCADE)
    city_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    city_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    city_lat = models.FloatField(blank=True, null=True, verbose_name="Ширина города")
    city_lon = models.FloatField(blank=True, null=True, verbose_name="Долгота города")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    phone = models.CharField(max_length=5, blank=True, verbose_name="Начало номера")

    class Meta:
        verbose_name="Местоположение 3"
        verbose_name_plural="Местоположения 3"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{}, {}, {}'.format(self.country_ru, self.region_ru, self.city_ru)

class IPUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_ip", verbose_name="Пользователь", on_delete=models.CASCADE)
    ip_1 = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 1")
    ip_2 = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 2")
    ip_3 = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 3")

    class Meta:
        verbose_name="ip пользователя"
        verbose_name_plural="ip пользователей"
        index_together = [('id', 'user'),]

    def __str__(self):
        return '{} - {}, {}, {}'.format(self.user.get_full_name(), self.ip_1, self.ip_2, self.ip_3)


class UserStaff(models.Model):
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
    level = models.CharField(max_length=5, choices=LEVEL, verbose_name="Уровень доступа")

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
    level = models.CharField(max_length=5, choices=LEVEL, verbose_name="Уровень доступа")

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
    level = models.CharField(max_length=5, choices=LEVEL, verbose_name="Уровень доступа")

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
    level = models.CharField(max_length=5, choices=LEVEL, verbose_name="Уровень доступа")

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
    level = models.CharField(max_length=5, choices=LEVEL, verbose_name="Уровень доступа")

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
    level = models.CharField(max_length=5, choices=LEVEL, verbose_name="Уровень доступа")

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

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала'
        verbose_name_plural = 'Создатели персонала'

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
