from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from managers.models import ModerationCategory
from logs.model.posts import PostManageLog


class ModeratedPost(models.Model):
    # рассмотрение жалобы на запись. Применение санкций или отвергание жалобы. При применении удаление жалоб-репортов
    STATUS_PENDING = 'P'
    STATUS_SUSPEND = 'S'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Запись рассматривается'),
        (STATUS_SUSPEND, 'Запись заморожена'),
        (STATUS_DELETED, 'Запись удалена'),
        (STATUS_REJECTED, 'Запись отвергнута'),
    )
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='moderated_post', blank=True, verbose_name="Запись")

    @classmethod
    def create_moderated_object(cls, post):
        return cls.objects.create(post=post)

    @classmethod
    def _get_or_create_moderated_object(cls, post):
        try:
            moderated_object = cls.objects.get(post=post)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(post=post)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_post(cls, post):
        return cls._get_or_create_moderated_object(post=post)

    @property
    def reports_count(self):
        # кол-во жалоб на пользователя
        return self.post_reports.count()

    def is_verified(self):
        # проверен ли пользователь
        return self.verified
    def is_suspend(self):
        # Объект заморожен
        return self.status == ModeratedPost.STATUS_SUSPEND
    def is_pending(self):
        # Жалоба рассматривается
        return self.status == ModeratedPost.STATUS_PENDING
    def is_deleted(self):
        # Объект блокирован
        return self.status == ModeratedPost.STATUS_DELETED

    def create_suspend(self, manager_id, post_id, severity_int):
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
        ModerationPenaltyPost.create_suspension_penalty(moderated_object=self, manager_id=manager_id, post_id=post_id, expiration=moderation_expiration)
        PostManageLog.objects.create(post_id=post_id, manager_id=manager_id, action_type=PostManageLog.SUSPENDED)
        self.save()
    def create_deleted(self, manager_id, post_id):
        self.verified = True
        self.save()
        ModerationPenaltyPost.create_block_penalty(moderated_object=self, manager_id=manager_id, post_id=post_id)
        PostManageLog.objects.create(post_id=post_id, manager_id=manager_id, action_type=PostManageLog.DELETED)

    def delete_suspend(self, manager_id, post_id):
        obj = ModerationPenaltyPost.objects.get(moderated_object=self, post_id=post_id)
        obj.delete()
        self.delete()
        PostManageLog.objects.create(post_id=post_id, manager_id=manager_id, action_type=PostManageLog.UNSUSPENDED)
    def delete_deleted(self, manager_id, post_id):
        obj = ModerationPenaltyPost.objects.get(moderated_object=self, post_id=post_id)
        obj.delete()
        self.delete()
        PostManageLog.objects.create(post=post, manager=manager, action_type=PostManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, post_id):
        self.verified = False
        self.post_moderated_object.all().delete()
        PostManageLog.objects.create(post_id=post_id, manager_id=manager_id, action_type=PostManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, post_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedPost.STATUS_REJECTED
        PostManageLog.objects.create(post_id=post_id, manager_id=manager_id, action_type=PostManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_post_id=self.pk).all()

    def __str__(self):
        return self.post.created

    class Meta:
        verbose_name = 'Проверяемая запись'
        verbose_name_plural = 'Проверяемые записи'


class PostModerationReport(models.Model):
    # жалобы на пользователя.
    PORNO = 'P'
    SPAM = 'S'
    BROKEN = 'B'
    FRAUD = 'P'
    CLON = 'K'
    OLD_PAGE = 'OP'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    PORNO = 'P'
    ARMS_SALE = 'AS'
    VIOLENCE = 'V'
    PERSECUTION = 'PE'
    SUICIDE = 'SU'
    PETS_ABUSE = 'PA'
    MISREPRESENTATION = "MI"
    EXTREMISM = "EX"
    NO_CHILD = 'NC'
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
        (ARMS_SALE, 'Продажа оружия'),
        (VIOLENCE, 'Насилие'),
        (PERSECUTION, 'Призыв к травле'),
        (SUICIDE, 'Призыв к суициду'),
        (PETS_ABUSE, 'Жестокое обращение c животными'),
        (MISREPRESENTATION, 'Введение в заблуждение'),
        (EXTREMISM, 'Экстремизм'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reports', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")

    @classmethod
    def create_post_moderation_report(cls, reporter_id, post, description, type):
        moderated_object = ModeratedPost.get_or_create_moderated_object_for_post(post=post)
        post_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return post_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на запись'
        verbose_name_plural = 'Жалобы на записи'


class ModerationPenaltyPost(models.Model):
    # сами санкции против пользователя. Пока только заморозка на разное время.
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='post_penalties', verbose_name="Оштрафованная запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_post_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_moderated_object', verbose_name="Объект")

    SUSPENSION = 'S'
    DELETE = 'D'
    BANNER = 'BA'
    TYPES = (
        (SUSPENSION, 'Приостановлено'),
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")

    @classmethod
    def create_suspension_penalty(cls, post_id, manager_id, moderated_object, expiration):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, post_id=post_id, type=cls.SUSPENSION, expiration=expiration)
    @classmethod
    def create_delete_penalty(cls, post_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, post_id=post_id, type=cls.DELETE)

    def is_suspend(self):
        # Объект заморожен
        return self.type == ModerationPenaltyPost.SUSPENSION
    def is_deleted(self):
        # Объект блокирован
        return self.type == ModerationPenaltyPost.DELETE

    def __str__(self):
        return self.post.created

    class Meta:
        verbose_name = 'Оштрафованная запись'
        verbose_name_plural = 'Оштрафованные записи'
