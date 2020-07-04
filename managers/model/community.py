from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from logs.model.user_community import CommunityManageLog
from communities.models import Community


class ModeratedCommunity(models.Model):
    # рассмотрение жалобы на сообщество. Применение санкций или отвергание жалобы. При применении удаление жалоб-репортов
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
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='moderated_community', blank=True, verbose_name="Сообщество")

    @classmethod
    def create_moderated_object(cls, community):
        return cls.objects.create(community=community)

    @classmethod
    def _get_or_create_moderated_object(cls, community):
        try:
            moderated_object = cls.objects.get(community=community)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(community=community)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_community(cls, community):
        return cls._get_or_create_moderated_object(community=community)

    @property
    def reports_count(self):
        # кол-во жалоб на пользователя
        return self.community_reports.count()

    def is_verified(self):
        # проверен ли пользователь
        return self.verified
    def is_suspend(self):
        # Объект заморожен
        return self.status == ModeratedCommunity.STATUS_SUSPEND
    def is_pending(self):
        # Жалоба рассматривается
        return self.status == ModeratedCommunity.STATUS_PENDING
    def is_bloked(self):
        # Объект блокирован
        return self.status == ModeratedCommunity.STATUS_BLOCKED
    def is_banner(self):
        # Объект блокирован
        return self.status == ModeratedCommunity.STATUS_BANNER_GET

    def create_suspend(self, manager_id, community_id, severity_int):
        self.verified = True
        severity = None
        duration_of_penalty = None
        if severity_int == '4':
            duration_of_penalty = timezone.timedelta(days=30)
            severity = "C"
        elif severity_int == '3':
            duration_of_penalty = timezone.timedelta(days=7)
            severity = "H"
        elif severity_int == '2':
            duration_of_penalty = timezone.timedelta(days=3)
            severity = "M"
        elif severity_int == '1':
            duration_of_penalty = timezone.timedelta(hours=6)
            severity = "L"
        moderation_expiration = timezone.now() + duration_of_penalty
        ModerationPenaltyCommunity.create_suspension_penalty(moderated_object=self, manager_id=manager_id, community_id=community_id, expiration=moderation_expiration)
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=severity)
        self.save()
    def create_block(self, manager_id, community_id):
        self.verified = True
        self.save()
        ModerationPenaltyCommunity.create_block_penalty(moderated_object=self, manager_id=manager_id, community_id=community_id)
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=CommunityManageLog.BLOCK)
    def create_warning_banner(self, manager_id, community_id):
        self.verified = True
        self.save()
        ModerationPenaltyCommunity.create_banner_penalty(moderated_object=self, manager_id=manager_id, community_id=community_id)
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=CommunityManageLog.WARNING_BANNER)

    def delete_suspend(self, manager_id, community_id):
        obj = ModerationPenaltyCommunity.objects.get(moderated_object=self, community_id=community_id)
        obj.delete()
        self.delete()
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=CommunityManageLog.UNSUSPENDED)
    def delete_block(self, manager_id, community_id):
        obj = ModerationPenaltyCommunity.objects.get(moderated_object=self, community_id=community_id)
        obj.delete()
        self.delete()
        CommunityManageLog.objects.create(community=community, manager=manager, action_type=CommunityManageLog.UNBLOCK)
    def delete_warning_banner(self, manager_id, community_id):
        obj = ModerationPenaltyCommunity.objects.get(moderated_object=self, community_id=community_id)
        obj.delete()
        self.delete()
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=CommunityManageLog.NO_WARNING_BANNER)

    def unverify_moderation(self, manager_id, community_id):
        self.verified = False
        self.community_moderated_object.all().delete()
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=CommunityManageLog.UNVERIFY)
        self.save()

    def suspend_moderation(self):
        current_status = self.status
        self.status = ModeratedCommunity.STATUS_SUSPEND
        self.save()

    def reject_moderation(self, manager_id, community_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedCommunity.STATUS_REJECTED
        CommunityManageLog.objects.create(community_id=community_id, manager_id=manager_id, action_type=CommunityManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(community_reports__moderated_community_id=self.pk).all()

    def __str__(self):
        return self.community.name

    class Meta:
        verbose_name = 'Модерируемое сообщество'
        verbose_name_plural = 'Модерируемые сообщества'


class CommunityModerationReport(models.Model):
    # жалобы на сообщество.
    PORNO = 'P'
    NO_CHILD = 'NC'
    SPAM = 'S'
    BROKEN = 'B'
    FRAUD = 'F'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    RHETORIC_HATE = "RH"
    UNETHICAL = "U"
    TYPE = (
        (PORNO, 'Порнография'),
        (NO_CHILD, 'Для взрослых'),
        (SPAM, 'Рассылка спама'),
        (BROKEN, 'Оскорбительное поведение'),
        (FRAUD, 'Мошенничество'),
        (DRUGS, 'Наркотики'),
        (NO_MORALITY, 'Не нравственный контент'),
        (RHETORIC_HATE, 'Риторика ненависти'),
        (UNETHICAL, 'Неэтичный контент'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_reports', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedCommunity, on_delete=models.CASCADE, related_name='community_reports', null=False, verbose_name="Сообщество")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")

    @classmethod
    def create_community_moderation_report(cls, reporter_id, community, description, type):
        moderated_object = ModeratedCommunity.get_or_create_moderated_object_for_community(community=community)
        community_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return community_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на сообщество'
        verbose_name_plural = 'Жалобы на сообщество'


class ModerationPenaltyCommunity(models.Model):
    # сами санкции против сообщества.
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_penalties', verbose_name="Оштрафованный сообщество")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedCommunity, on_delete=models.CASCADE, related_name='community_moderated_object', verbose_name="Объект")

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
    def create_suspension_penalty(cls, community_id, manager_id, moderated_object, expiration):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, community_id=community_id, type=cls.SUSPENSION, expiration=expiration)
    @classmethod
    def create_block_penalty(cls, community_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, community_id=community_id, type=cls.BLOCK)
    @classmethod
    def create_banner_penalty(cls, community_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, community_id=community_id, type=cls.BANNER)

    def is_suspend(self):
        # Объект заморожен
        return self.type == ModerationPenaltyCommunity.SUSPENSION
    def is_bloked(self):
        # Объект блокирован
        return self.type == ModerationPenaltyCommunity.BLOCK
    def is_banner(self):
        # Объект блокирован
        return self.type == ModerationPenaltyCommunity.BANNER

    def __str__(self):
        return self.community.name

    class Meta:
        verbose_name = 'Оштрафованное сообщество'
        verbose_name_plural = 'Оштрафованные сообщества'
