from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.conf import settings


class PlannerManageLog(models.Model):
    WORKSPACE_CLOSED, BOARD_CLOSED, COLUMN_CLOSED, CARD_CLOSED, COMMENT_CLOSED = 1,2,3,4,5
    WORKSPACE_CLOSED_HIDE, BOARD_CLOSED_HIDE, COLUMN_CLOSED_HIDE, CARD_CLOSED_HIDE, COMMENT_CLOSED_HIDE = 8, 9,10,11,12
    WORKSPACE_REJECT, BOARD_REJECT, COLUMN_REJECT, CARD_REJECT, COMMENT_REJECT = 16, 17,18,19,20
    WORKSPACE_UNVERIFY, BOARD_UNVERIFY, COLUMN_UNVERIFY, CARD_UNVERIFY, COMMENT_UNVERIFY = 25, 26,27,28,29
    ACTION_TYPES = (
        (WORKSPACE_CLOSED, 'Рабочее пространство закрыто'),
        (BOARD_CLOSED, 'Доска закрыта'),
        (COLUMN_CLOSED, 'Колонка закрыта'),
        (CARD_CLOSED, 'Карточка закрыта'),
        (COMMENT_CLOSED, 'Комментарий закрыт'),

        (WORKSPACE_CLOSED_HIDE, 'Рабочее пространство восстановлено'),
        (BOARD_CLOSED_HIDE, 'Доска восстановлена'),
        (COLUMN_CLOSED_HIDE, 'Колонка восстановлена'),
        (CARD_CLOSED_HIDE, 'Карточка восстановлена'),
        (COMMENT_CLOSED_HIDE, 'Комментарий восстановлен'),

        (WORKSPACE_REJECT, 'Жалоба на рабочее пространство отклонена'),
        (BOARD_REJECT, 'Жалоба на доску отклонена'),
        (COLUMN_REJECT, 'Жалоба на колонку отклонена'),
        (CARD_REJECT, 'Жалоба на карточку отклонена'),
        (COMMENT_REJECT, 'Жалоба на комментарий отклонена'),

        (WORKSPACE_UNVERIFY, 'Проверка на рабочее пространство убрана'),
        (BOARD_UNVERIFY, 'Проверка на доску убрана'),
        (COLUMN_UNVERIFY, 'Проверка на колонку убрана'),
        (CARD_UNVERIFY, 'Проверка на карточку убрана'),
        (COMMENT_UNVERIFY, 'Проверка на комментарий убрана'),
    )
    item = models.PositiveIntegerField(default=0, verbose_name="Элемент планировщика")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.PositiveSmallIntegerField(default=0, choices=ACTION_TYPES, verbose_name="Статус")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог менеджера планировщика"
        verbose_name_plural = "Логи менеджеров планировщика"
        ordering=["-created"]


class PlannerWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен админ планировщика'),
        (DELETE_ADMIN, 'Удален админ планировщика'),
        (CREATE_EDITOR, 'Добавлен редактор планировщика'),
        (DELETE_EDITOR, 'Удален редактор планировщика'),
        (CREATE_MODERATOR, 'Добавлен модератор планировщика'),
        (DELETE_MODERATOR, 'Удален модератор планировщика'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.PositiveSmallIntegerField(default=0, choices=ACTION_TYPES)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог суперменеджера планировщика"
        verbose_name_plural = "Логи суперменеджеров планировщика"
        ordering=["-created"]

class PlannerCreateWorkerManageLog(models.Model):
    CREATE_ADMIN = 'CA'
    DELETE_ADMIN = 'DA'
    CREATE_EDITOR = 'CE'
    DELETE_EDITOR = 'DE'
    CREATE_MODERATOR = 'CM'
    DELETE_MODERATOR = 'DM'
    ACTION_TYPES = (
        (CREATE_ADMIN, 'Добавлен создатель админов планировщика'),
        (DELETE_ADMIN, 'Удален создатель админов планировщика'),
        (CREATE_EDITOR, 'Добавлен создатель редакторов планировщика'),
        (DELETE_EDITOR, 'Удален создатель редакторов планировщика'),
        (CREATE_MODERATOR, 'Добавлен создатель модераторов планировщика'),
        (DELETE_MODERATOR, 'Удален создатель модераторов планировщика'),
    )

    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    manager = models.PositiveIntegerField(default=0, verbose_name="Менеджер")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    action_type = models.PositiveSmallIntegerField(default=0, choices=ACTION_TYPES)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "Лог создателя суперменеджера планировщика"
        verbose_name_plural = "Логи создателей суперменеджеров планировщика"
        ordering=["-created"]
