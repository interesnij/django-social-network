from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex


class UserNumbers(models.Model):
    visitor = models.PositiveIntegerField(default=0, verbose_name="Кто заходит")
    target = models.PositiveIntegerField(default=0, verbose_name="К кому заходит")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Кто к кому заходил"
        verbose_name_plural = "Кто к кому заходил"


class CommunityNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто заходит")
    community = models.PositiveIntegerField(default=0, verbose_name="В какое сообщество заходил")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        #ordering = ['-created']
        verbose_name = "Посещение сообщества"
        verbose_name_plural = "Посещения сообщества"


class GoodNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    good = models.PositiveIntegerField(default=0, verbose_name="Какой товар смотрит")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Посещение товара"
        verbose_name_plural = "Посещения товара"


class VideoNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    video = models.PositiveIntegerField(default=0, verbose_name="Какой ролик смотрит")
    platform = models.PositiveIntegerField(default=0, verbose_name="0 Комп, 1 Телефон")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Просмотр ролика"
        verbose_name_plural = "Просмотры ролика"


class MusicNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто слушает")
    music = models.PositiveIntegerField(default=0, verbose_name="Какой трек слушает")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Прослушивание трека"
        verbose_name_plural = "Прослушивания трека"


class PostNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    post = models.PositiveIntegerField(default=0, verbose_name="Какую запись смотрит")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Охват записи на стене и в лентах"
        verbose_name_plural = "Охват записей на стене и в лентах"

class PostAdNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    post = models.PositiveIntegerField(default=0, verbose_name="Какую запись смотрит")
    created = models.DateField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Охват рекламной записи на стене и в лентах"
        verbose_name_plural = "Охват рекламных записей на стене и в лентах"
