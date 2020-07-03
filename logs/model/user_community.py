from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class UserManageLog(models.Model):
    REMOVE = 'R'
    UNREMOVE = 'UR'
    BLOCK = 'B'
    UNBLOCK = 'UB'
    SEVERITY_CRITICAL = 'C'
    SEVERITY_HIGH = 'H'
    SEVERITY_MEDIUM = 'M'
    SEVERITY_LOW = 'L'
    UNSUSPENDED = 'US'
    WARNING_BANNER = 'WB'
    NO_WARNING_BANNER = 'NWB'
    REJECT = 'R'
    UNVERIFY = 'UV'
    ACTION_TYPES = (
        (REMOVE, 'Удален'),
        (UNREMOVE, 'Восстановлен'),
        (BLOCK, 'Заблокирован'),
        (UNBLOCK, 'Разблокирован'),
        (SEVERITY_CRITICAL, 'Вечная заморозка'),
        (SEVERITY_HIGH, 'Долгая заморозка'),
        (SEVERITY_MEDIUM, 'Средняя заморозка'),
        (SEVERITY_LOW, 'Краткая заморозка'),
        (UNSUSPENDED, 'Разморожен'),
        (WARNING_BANNER, 'Выставлен предупреждающий баннер'),
        (NO_WARNING_BANNER, 'Убран предупреждающий баннер'),
        (REJECT, 'Жалоба отклонена'),
        (UNVERIFY, 'Проверка убрана'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера пользоватетей"
        verbose_name_plural = "Логи менеджеров пользоватетей"
        ordering=["-created"]

class CommunityManageLog(models.Model):
    REMOVE = 'R'
    UNREMOVE = 'UR'
    BLOCK = 'B'
    UNBLOCK = 'UB'
    SUSPENDED = 'S'
    UNSUSPENDED = 'US'
    WARNING_BANNER = 'WB'
    NO_WARNING_BANNER = 'NWB'
    REJECT = 'R'
    UNVERIFY = 'UV'
    ACTION_TYPES = (
        (REMOVE, 'Удалено'),
        (UNREMOVE, 'Восстановлено'),
        (BLOCK, 'Заблокировано'),
        (UNBLOCK, 'Разблокировано'),
        (SUSPENDED, 'Заморожено'),
        (UNSUSPENDED, 'Разморожено'),
        (WARNING_BANNER, 'Выставлен предупреждающий баннер'),
        (NO_WARNING_BANNER, 'Убран предупреждающий баннер'),
        (REJECT, 'Жалоба отклонена'),
        (UNVERIFY, 'Проверка убрана'),
    )

    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, verbose_name="Сообщество")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="community_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера пользоватетей"
        verbose_name_plural = "Логи менеджеров пользоватетей"
        ordering=["-created"]


class UserWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    CREATE_ADVERTISER = 'CR'
    DELETE_ADVERTISER = 'DR'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ пользователей'),
        (DELETE_ADMIN, 'Удален админ пользователей'),
        (CREATE_EDITOR, 'Добавлен редактор пользователей'),
        (DELETE_EDITOR, 'Удален редактор пользователей'),
        (CREATE_MODERATOR, 'Добавлен модератор пользователей'),
        (DELETE_MODERATOR, 'Удален модератор пользователей'),
        (CREATE_ADVERTISER, 'Добавлен менеджер рекламодателей пользователей'),
        (DELETE_ADVERTISER, 'Удален менеджер рекламодателей пользователей'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера пользоватетей"
        verbose_name_plural = "Логи менеджеров пользоватетей"
        ordering=["-created"]

class UserCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    CREATE_ADVERTISER = 'CR'
    DELETE_ADVERTISER = 'DR'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов пользователей'),
        (DELETE_ADMIN, 'Удален создатель админов пользователей'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов пользователей'),
        (DELETE_EDITOR, 'Удален создатель редакторов пользователей'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов пользователей'),
        (DELETE_MODERATOR, 'Удален создатель модераторов пользователей'),
        (CREATE_ADVERTISER, 'Добавлен создатель менеджеров рекламодателей пользователей'),
        (DELETE_ADVERTISER, 'Удален создатель менеджеров рекламодателей пользователей'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_creator_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя менеджера пользоватетей"
        verbose_name_plural = "Логи создателей менеджеров пользоватетей"
        ordering=["-created"]


class CommunityWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    CREATE_ADVERTISER = 'CR'
    DELETE_ADVERTISER = 'DR'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ сообществ'),
        (DELETE_ADMIN, 'Удален админ сообществ'),
        (CREATE_EDITOR, 'Добавлен редактор сообществ'),
        (DELETE_EDITOR, 'Удален редактор сообществ'),
        (CREATE_MODERATOR, 'Добавлен модератор сообществ'),
        (DELETE_MODERATOR, 'Удален модератор сообществ'),
        (CREATE_ADVERTISER, 'Добавлен менеджер рекламодателей сообществ'),
        (DELETE_ADVERTISER, 'Удален менеджер рекламодателей сообществ'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Сообщество")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="community_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера сообществ"
        verbose_name_plural = "Логи менеджеров сообществ"
        ordering=["-created"]

class CommunityCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    CREATE_ADVERTISER = 'CR'
    DELETE_ADVERTISER = 'DR'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов сообществ'),
        (DELETE_ADMIN, 'Удален создатель админов сообществ'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов сообществ'),
        (DELETE_EDITOR, 'Удален создатель редакторов сообществ'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов сообществ'),
        (DELETE_MODERATOR, 'Удален создатель модераторов сообществ'),
        (CREATE_ADVERTISER, 'Добавлен создатель менеджеров рекламодателей сообществ'),
        (DELETE_ADVERTISER, 'Удален создатель менеджеров рекламодателей сообществ'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Сообщество")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="community_creator_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя менеджера сообществ"
        verbose_name_plural = "Логи создателей менеджеров сообществ"
        ordering=["-created"]
