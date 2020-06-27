from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class VideoManageLog(models.Model):
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

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Запись")
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
        verbose_name = "Лог менеджера видеороликов"
        verbose_name_plural = "Логи менеджеров видеороликов"
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
        verbose_name = "Лог создателя менеджера видеороликов"
        verbose_name_plural = "Логи создателей менеджеров видеороликов"
        ordering=["-created"]
