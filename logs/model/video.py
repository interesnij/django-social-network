from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class VideoManageLog(models.Model):
    DELETED = 'D'
    UNDELETED = 'UD'
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

    video = models.PositiveIntegerField(default=0, verbose_name="Запись")
    manager = models.PositiveIntegerField(default=0, on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера видеороликов"
        verbose_name_plural = "Логи менеджеров видеороликов"
        ordering=["-created"]


class VideoCommentManageLog(models.Model):
    DELETED = 'D'
    UNDELETED = 'UD'
    REJECT = 'R'
    UNVERIFY = 'UV'
    ACTION_TYPES = (
        (DELETED, 'Удален'),
        (UNDELETED, 'Восстановлен'),
        (REJECT, 'Жалоба отклонена'),
        (UNVERIFY, 'Проверка убрана'),
    )

    comment = models.PositiveIntegerField(default=0, verbose_name="Комментарий к видеоролику")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

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

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

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

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера видеороликов"
        verbose_name_plural = "Логи создателей суперменеджеров видеороликов"
        ordering=["-created"]
