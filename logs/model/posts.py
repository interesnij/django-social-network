from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class PostManageLog(models.Model):
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

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, verbose_name="Запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера записи"
        verbose_name_plural = "Логи менеджеров записей"
        ordering=["-created"]


class PostCommentManageLog(models.Model):
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

    comment = models.ForeignKey('posts.PostComment', on_delete=models.CASCADE, verbose_name="Комментарий к записи")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_comment_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера комментария"
        verbose_name_plural = "Логи менеджеров комментариев"
        ordering=["-created"]

class PostWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ записей'),
        (DELETE_ADMIN, 'Удален админ записей'),
        (CREATE_EDITOR, 'Добавлен редактор записей'),
        (DELETE_EDITOR, 'Удален редактор записей'),
        (CREATE_MODERATOR, 'Добавлен модератор записей'),
        (DELETE_MODERATOR, 'Удален модератор записей'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_worker_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера записей"
        verbose_name_plural = "Логи суперменеджеров записей"
        ordering=["-created"]

class PostCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов записей'),
        (DELETE_ADMIN, 'Удален создатель админов записей'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов записей'),
        (DELETE_EDITOR, 'Удален создатель редакторов записей'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов записей'),
        (DELETE_MODERATOR, 'Удален создатель модераторов записей'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_create_manager", on_delete=models.CASCADE, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера записей"
        verbose_name_plural = "Логи создателей суперменеджеров записей"
        ordering=["-created"]
