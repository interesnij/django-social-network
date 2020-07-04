from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class VideoManageLog(models.Model):
    DELETED = 'D'
    UNDELETED = 'UD'
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

    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, verbose_name="Запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера видеороликов"
        verbose_name_plural = "Логи менеджеров видеороликов"
        ordering=["-created"]

class VideoWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ видеороликов'),
        (DELETE_ADMIN, 'Удален админ видеороликов'),
        (CREATE_EDITOR, 'Добавлен редактор видеороликов'),
        (DELETE_EDITOR, 'Удален редактор видеороликов'),
        (CREATE_MODERATOR, 'Добавлен модератор видеороликов'),
        (DELETE_MODERATOR, 'Удален модератор видеороликов'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера видеороликов"
        verbose_name_plural = "Логи суперменеджеров видеороликов"
        ordering=["-created"]

class VideoCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов видеороликов'),
        (DELETE_ADMIN, 'Удален создатель админов видеороликов'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов видеороликов'),
        (DELETE_EDITOR, 'Удален создатель редакторов видеороликов'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов видеороликов'),
        (DELETE_MODERATOR, 'Удален создатель модераторов видеороликов'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_create_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера видеороликов"
        verbose_name_plural = "Логи создателей суперменеджеров видеороликов"
        ordering=["-created"]
