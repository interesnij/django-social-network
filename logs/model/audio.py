from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class AudioManageLog(models.Model):
    REMOVE = 'R'
    UNREMOVE = 'UR'
    BLOCK = 'B'
    UNBLOCK = 'UB'
    SUSPENDED = 'S'
    UNSUSPENDED = 'US'
    ACTION_TYPES = (
        (REMOVE, 'Удален'),
        (UNREMOVE, 'Восстановлен'),
        (BLOCK, 'Заблокирован'),
        (UNBLOCK, 'Разблокирован'),
        (SUSPENDED, 'Заморожен'),
        (UNSUSPENDED, 'Разморожен'),
    )

    audio = models.ForeignKey('music.SoundcloudParsing', on_delete=models.CASCADE, verbose_name="Запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="audio_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="audio_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера аудиозаписей"
        verbose_name_plural = "Логи менеджеров аудиозаписей"
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="audio_create_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя менеджера аудиозаписей"
        verbose_name_plural = "Логи создателей менеджеров аудиозаписей"
        ordering=["-created"]
