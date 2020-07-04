from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class GoodManageLog(models.Model):
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

    post = models.ForeignKey('goods.Good', on_delete=models.CASCADE, verbose_name="Запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера товаров"
        verbose_name_plural = "Логи менеджеров товаров"
        ordering=["-created"]

class GoodWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ товаров'),
        (DELETE_ADMIN, 'Удален админ товаров'),
        (CREATE_EDITOR, 'Добавлен редактор товаров'),
        (DELETE_EDITOR, 'Удален редактор товаров'),
        (CREATE_MODERATOR, 'Добавлен модератор товаров'),
        (DELETE_MODERATOR, 'Удален модератор товаров'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера товаров"
        verbose_name_plural = "Логи суперменеджеров товаров"
        ordering=["-created"]

class GoodCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов товаров'),
        (DELETE_ADMIN, 'Удален создатель админов товаров'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов товаров'),
        (DELETE_EDITOR, 'Удален создатель редакторов товаров'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов товаров'),
        (DELETE_MODERATOR, 'Удален создатель модераторов товаров'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_create_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера товаров"
        verbose_name_plural = "Логи создателей суперменеджеров товаров"
        ordering=["-created"]
