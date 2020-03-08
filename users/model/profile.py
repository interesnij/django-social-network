from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, db_index=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, db_index=False, related_name="profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    bio = models.TextField(max_length=settings.PROFILE_BIO_MAX_LENGTH, blank=True, verbose_name="Биография")
    sity = models.CharField(max_length=settings.PROFILE_LOCATION_MAX_LENGTH, blank=True, verbose_name="Местоположение")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    vk_url = models.URLField(blank=True, verbose_name="Ссылка на vk")
    youtube_url = models.URLField(blank=True, verbose_name="Ссылка на youtube")
    facebook_url = models.URLField(blank=True, verbose_name="Ссылка на facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Ссылка на instagram")
    twitter_url = models.URLField(blank=True, verbose_name="Ссылка на twitter")
    phone = models.CharField(max_length=15,blank=True, verbose_name="Телефон")


    def __str__(self):
        return self.user.last_name

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        index_together = [('id', 'user'),]

class OneUserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_location", verbose_name="Пользователь", on_delete=models.CASCADE)
    sity_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    sity_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Местоположение и ip пользователя"
        verbose_name_plural="Местоположения и ip пользователей"

class TwoUserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_location_2", verbose_name="Пользователь", on_delete=models.CASCADE)
    sity_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    sity_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Местоположение и ip пользователя"
        verbose_name_plural="Местоположения и ip пользователей"

class ThreeUserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_location_3", verbose_name="Пользователь", on_delete=models.CASCADE)
    sity_ru = models.CharField(max_length=100, blank=True, verbose_name="Город по-русски")
    sity_en = models.CharField(max_length=100, blank=True, verbose_name="Город по-английски")
    region_ru = models.CharField(max_length=100, blank=True, verbose_name="Регион по-русски")
    region_en = models.CharField(max_length=100, blank=True, verbose_name="Регион по-английски")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Страна по-русски")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Страна по-английски")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Местоположение и ip пользователя"
        verbose_name_plural="Местоположения и ip пользователей"

class IPUser(models.Model):
    ip_1 = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 1")
    ip_2 = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 2")
    ip_3 = models.GenericIPAddressField(protocol='both', null=True, blank=True, verbose_name="ip 3")
