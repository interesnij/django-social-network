from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex


class UserNumbers(models.Model):
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visitor_user', verbose_name="Кто заходит")
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='target_user', verbose_name="К кому заходит")
    count = models.PositiveIntegerField(default=0, verbose_name="Кол-во визитов")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        unique_together = ('visitor', 'target',)
        verbose_name="Кто к кому заходил"
        verbose_name_plural="Кто к кому заходил"


class CommuityNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто заходит")
    community = models.PositiveIntegerField(default=0, verbose_name="В какое сообщество заходил")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Посещение сообщества"
        verbose_name_plural="Посещения сообщества"


class GoodNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    good = models.PositiveIntegerField(default=0, verbose_name="Какой товар смотрит")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Посещение товара"
        verbose_name_plural="Посещения товара"


class VideoNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    video = models.PositiveIntegerField(default=0, verbose_name="Какой ролик смотрит")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Просмотр ролика"
        verbose_name_plural="Просмотры ролика"


class MusicNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто слушает")
    music = models.PositiveIntegerField(default=0, verbose_name="Какой трек слушает")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Прослушивание трека"
        verbose_name_plural="Прослушивания трека"


class ItemNumbers(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Кто смотрит")
    music = models.PositiveIntegerField(default=0, verbose_name="Какую запись смотрит")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="Просмотр записи"
        verbose_name_plural="Просмотры записи"
