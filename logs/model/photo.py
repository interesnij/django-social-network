from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class PhotoManageLog(models.Model):
    DELETED = 'R'
    UNDELETED = 'UR'
    BLOCK = 'B'
    UNBLOCK = 'UB'
    SEVERITY_CRITICAL = 'C'
    SEVERITY_HIGH = 'H'
    SEVERITY_MEDIUM = 'M'
    SEVERITY_LOW = 'L'
    UNSUSPENDED = 'US'
    ACTION_TYPES = (
        (DELETED, 'Удален'),
        (UNDELETED, 'Восстановлен'),
        (BLOCK, 'Заблокирован'),
        (UNBLOCK, 'Разблокирован'),
        (SEVERITY_CRITICAL, 'Вечная заморозка'),
        (SEVERITY_HIGH, 'Долгая заморозка'),
        (SEVERITY_MEDIUM, 'Средняя заморозка'),
        (SEVERITY_LOW, 'Краткая заморозка'),
        (UNSUSPENDED, 'Разморожен'),
    )

    photo = models.ForeignKey('gallery.Photo', on_delete=models.CASCADE, verbose_name="Запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера фотографий"
        verbose_name_plural = "Логи менеджеров фотографий"
        ordering=["-created"]

class PhotoWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ фотографий'),
        (DELETE_ADMIN, 'Удален админ фотографий'),
        (CREATE_EDITOR, 'Добавлен редактор фотографий'),
        (DELETE_EDITOR, 'Удален редактор фотографий'),
        (CREATE_MODERATOR, 'Добавлен модератор фотографий'),
        (DELETE_MODERATOR, 'Удален модератор фотографий'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера фотографий"
        verbose_name_plural = "Логи суперменеджеров фотографий"
        ordering=["-created"]

class PhotoCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов фотографий'),
        (DELETE_ADMIN, 'Удален создатель админов фотографий'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов фотографий'),
        (DELETE_EDITOR, 'Удален создатель редакторов фотографий'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов фотографий'),
        (DELETE_MODERATOR, 'Удален создатель модераторов фотографий'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="photo_create_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера фотографий"
        verbose_name_plural = "Логи создателей суперменеджеров фотографий"
        ordering=["-created"]
