from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from managers.models import ModerationCategory
from logs.model.user_community import UserManageLog


class ModeratedUser(models.Model):
    # рассмотрение жалобы на пользователя. Применение санкций или отвергание жалобы. При применении удаление жалоб-репортов
    STATUS_PENDING = 'P'
    STATUS_SUSPEND = 'S'
    STATUS_BLOCKED = 'B'
    STATUS_BANNER_GET = 'BG'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_SUSPEND, 'Объект заморожен'),
        (STATUS_BLOCKED, 'Объект заблокирован'),
        (STATUS_BANNER_GET, 'Объекту присвоен баннер'),
        (STATUS_REJECTED, 'Отвергнутый'),
    )
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='moderated_user', blank=True, verbose_name="Пользователь")

    @classmethod
    def create_moderated_object(cls, user):
        return cls.objects.create(user=user)

    @classmethod
    def _get_or_create_moderated_object(cls, user):
        try:
            moderated_object = cls.objects.get(user=user)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(user=user)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_user(cls, user):
        return cls._get_or_create_moderated_object(user=user)

    @property
    def reports_count(self):
        # кол-во жалоб на пользователя
        return self.user_reports.count()

    def is_verified(self):
        # проверен ли пользователь
        return self.verified
    def is_suspend(self):
        # Объект заморожен
        return self.status == ModeratedUser.STATUS_SUSPEND
    def is_pending(self):
        # Жалоба рассматривается
        return self.status == ModeratedUser.STATUS_PENDING
    def is_bloked(self):
        # Объект блокирован
        return self.status == ModeratedUser.STATUS_BLOCKED
    def is_banner(self):
        # Объект блокирован
        return self.status == ModeratedUser.STATUS_BANNER_GET

    def create_suspend(self, manager_id, user_id, severity_int):
        self.verified = True
        severity = None
        duration_of_penalty = None
        if severity_int == '4':
            duration_of_penalty = timezone.timedelta(days=30)
            severity = "C"
        elif severity_int == '3':
            severity_int = timezone.timedelta(days=7)
            severity = "H"
        elif severity_int == '2':
            duration_of_penalty = timezone.timedelta(days=3)
            severity = "M"
        elif severity_int == '1':
            duration_of_penalty = timezone.timedelta(hours=6)
            severity = "L"
        moderation_expiration = timezone.now() + duration_of_penalty
        ModerationPenaltyUser.create_suspension_penalty(moderated_object=self, type=ModerationPenaltyUser.SUSPENSION, manager_id=manager_id, user_id=user_id, expiration=moderation_expiration)
        UserManageLog.objects.create(user=user,manager=manager,action_type=severity)
        self.save()
    def create_block(self, manager_id, user_id):
        self.verified = True
        ModerationPenaltyUser.create_block_penalty(moderated_object=self, type=ModerationPenaltyUser.BLOCK, manager_id=manager.pk, user_id=user.pk)
        UserManageLog.objects.create(user=user,manager=manager,action_type=UserManageLog.BLOCK)
    def create_warning_banner(self, manager_id, user_id):
        self.verified = True
        ModerationPenaltyUser.create_banner_penalty(moderated_object=self, type=ModerationPenaltyUser.BANNER, manager_id=manager.pk, user_id=user.pk)
        UserManageLog.objects.create(user=user,manager=manager,action_type=UserManageLog.WARNING_BANNER)

    def delete_suspend(self, manager_id, user_id):
        obj = ModerationPenaltyUser.objects.get(moderated_object=self, user_id=user.pk)
        obj.delete()
        UserManageLog.objects.create(user=user,manager=manager,action_type=UserManageLog.UNSUSPENDED)
    def delete_block(self, manager_id, user_id):
        obj = ModerationPenaltyUser.objects.get(moderated_object=self, user_id=user.pk)
        obj.delete()
        UserManageLog.objects.create(user=user,manager=manager,action_type=UserManageLog.UNBLOCK)
    def delete_warning_banner(self, manager_id, user_id):
        obj = ModerationPenaltyUser.objects.get(moderated_object=self, user_id=user.pk)
        obj.delete()
        UserManageLog.objects.create(user=user,manager=manager,action_type=UserManageLog.NO_WARNING_BANNER)

    def unverify_moderation(self):
        self.verified = False
        self.user_penalties.all().delete()
        self.save()

    def suspend_moderation(self):
        current_status = self.status
        self.status = ModeratedUser.STATUS_SUSPEND
        self.save()

    def reject_moderation(self, manager_id, user_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedUser.STATUS_REJECTED
        UserManageLog.objects.create(user=user,manager=manager,action_type=UserManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_user_id=self.pk).all()

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Модерируемый пользователь'
        verbose_name_plural = 'Модерируемые пользователи'


class UserModerationReport(models.Model):
    # жалобы на пользователя.
    PORNO = 'P'
    NO_CHILD = 'NC'
    SPAM = 'S'
    BROKEN = 'B'
    FRAUD = 'P'
    CLON = 'K'
    OLD_PAGE = 'OP'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    PORNO = 'P'
    TYPE = (
        (PORNO, 'Порнография'),
        (NO_CHILD, 'Для взрослых'),
        (SPAM, 'Рассылка спама'),
        (BROKEN, 'Оскорбительное поведение'),
        (FRAUD, 'Мошенничество'),
        (CLON, 'Клон моей страницы'),
        (OLD_PAGE, 'Моя старая страница'),
        (DRUGS, 'Наркотики'),
        (NO_MORALITY, 'Не нравственный контент'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reports', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedUser, on_delete=models.CASCADE, related_name='user_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")

    @classmethod
    def create_user_moderation_report(cls, reporter_id, user, description):
        moderated_object = ModeratedUser.get_or_create_moderated_object_for_user(user=user)
        user_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return user_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба пользователя'
        verbose_name_plural = 'Жалобы пользователей'


class ModerationPenaltyUser(models.Model):
    # сами санкции против пользователя. Пока только заморозка на разное время.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_penalties', verbose_name="Оштрафованный пользователь")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedUser, on_delete=models.CASCADE, related_name='user_moderated_object', verbose_name="Объект")

    SUSPENSION = 'S'
    BLOCK = 'B'
    BANNER = 'BA'
    TYPES = (
        (SUSPENSION, 'Приостановлено'),
        (BLOCK, 'Заблокировано'),
        (BANNER, 'Вывешен баннер'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")

    @classmethod
    def create_suspension_penalty(cls, user_id, manager_id, moderated_object, expiration):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, user_id=user_id, type=cls.SUSPENSION, expiration=expiration)
    @classmethod
    def create_block_penalty(cls, user_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, user_id=user_id, type=cls.BLOCK)
    @classmethod
    def create_banner_penalty(cls, user_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, user_id=user_id, type=cls.BANNER)

    def is_suspend(self):
        # Объект заморожен
        return self.type == ModerationPenaltyUser.SUSPENSION
    def is_bloked(self):
        # Объект блокирован
        return self.type == ModerationPenaltyUser.BLOCK
    def is_banner(self):
        # Объект блокирован
        return self.type == ModerationPenaltyUser.BANNER

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный пользователь'
        verbose_name_plural = 'Оштрафованные пользователи'
