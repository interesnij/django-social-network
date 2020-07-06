from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class AudioManageLog(models.Model):
    DELETED = 'R'
    UNDELETED = 'UR'
    SEVERITY_CRITICAL = 'C'
    SEVERITY_HIGH = 'H'
    SEVERITY_MEDIUM = 'M'
    SEVERITY_LOW = 'L'
    UNSUSPENDED = 'US'
    REJECT = 'R'
    UNVERIFY = 'UV'
    ACTION_TYPES = (
        (DELETED, 'Удален'),
        (UNDELETED, 'Восстановлен'),
        (SEVERITY_CRITICAL, 'Вечная заморозка'),
        (SEVERITY_HIGH, 'Долгая заморозка'),
        (SEVERITY_MEDIUM, 'Средняя заморозка'),
        (SEVERITY_LOW, 'Краткая заморозка'),
        (UNSUSPENDED, 'Разморожен'),
        (REJECT, 'Жалоба отклонена'),
        (UNVERIFY, 'Проверка убрана'),
    )

    audio = models.PositiveIntegerField(default=0, verbose_name="Запись")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера аудиозаписей"
        verbose_name_plural = "Логи менеджеров аудиозаписей"
        ordering=["-created"]


class AudioWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ аудиозаписей'),
        (DELETE_ADMIN, 'Удален админ аудиозаписей'),
        (CREATE_EDITOR, 'Добавлен редактор аудиозаписей'),
        (DELETE_EDITOR, 'Удален редактор аудиозаписей'),
        (CREATE_MODERATOR, 'Добавлен модератор аудиозаписей'),
        (DELETE_MODERATOR, 'Удален модератор аудиозаписей'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера аудиозаписей"
        verbose_name_plural = "Логи супеменеджеров аудиозаписей"
        ordering=["-created"]

class AudioCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов аудиозаписей'),
        (DELETE_ADMIN, 'Удален создатель админов аудиозаписей'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов аудиозаписей'),
        (DELETE_EDITOR, 'Удален создатель редакторов аудиозаписей'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов аудиозаписей'),
        (DELETE_MODERATOR, 'Удален создатель модераторов аудиозаписей'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера аудиозаписей"
        verbose_name_plural = "Логи создателей суперменеджеров аудиозаписей"
        ordering=["-created"]
