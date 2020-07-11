from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from logs.model.manage_goods import GoodManageLog, GoodCommentManageLog


class ModeratedGood(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Товар рассматривается'),
        (STATUS_DELETED, 'Товар удален'),
        (STATUS_REJECTED, 'Товар отвергнут'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    good = models.ForeignKey('goods.Good', on_delete=models.CASCADE, related_name='moderated_good', blank=True, verbose_name="Товар")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_moderated_object(cls, good):
        return cls.objects.create(good=good)

    @classmethod
    def _get_or_create_moderated_object(cls, good):
        try:
            moderated_object = cls.objects.get(good=good)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(good=good)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_good(cls, good):
        return cls._get_or_create_moderated_object(good=good)

    @property
    def reports_count(self):
        return self.good_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedGood.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedGood.STATUS_DELETED

    def create_deleted(self, manager_id, good_id):
        self.verified = True
        self.save()
        ModerationPenaltyGood.create_delete_penalty(moderated_object=self, manager_id=manager_id, good_id=good_id)
        GoodManageLog.objects.create(good=good_id, manager=manager_id, action_type=GoodManageLog.DELETED)

    def delete_deleted(self, manager_id, good_id):
        obj = ModerationPenaltyGood.objects.get(moderated_object=self, good_id=good_id)
        obj.delete()
        self.delete()
        GoodManageLog.objects.create(good=good_id, manager=manager_id, action_type=GoodManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, good_id):
        self.verified = False
        self.good_moderated_object.all().delete()
        GoodManageLog.objects.create(good=good_id, manager=manager_id, action_type=GoodManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, good_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedGood.STATUS_REJECTED
        GoodManageLog.objects.create(good=good_id, manager=manager_id, action_type=GoodManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_good_id=self.pk).all()

    def __str__(self):
        return self.good.creator.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый товар'
        verbose_name_plural = 'Проверяемые товар'


class ModeratedGoodComment(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Товар рассматривается'),
        (STATUS_DELETED, 'Товар удален'),
        (STATUS_REJECTED, 'Товар отвергнут'),
    )
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    comment = models.ForeignKey('goods.GoodComment', on_delete=models.CASCADE, related_name='moderated_good_comment', blank=True, verbose_name="Комментарий к товару")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_moderated_object(cls, comment):
        return cls.objects.create(comment=comment)

    @classmethod
    def _get_or_create_moderated_object(cls, comment):
        try:
            moderated_object = cls.objects.get(comment=comment)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(comment=comment)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_comment(cls, comment):
        return cls._get_or_create_moderated_object(comment=comment)

    @property
    def reports_count(self):
        return self.good_comment_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedGoodComment.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedGoodComment.STATUS_DELETED

    def create_deleted(self, manager_id, comment_id):
        self.verified = True
        self.save()
        ModerationPenaltyGoodComment.create_delete_penalty(moderated_object=self, manager_id=manager_id, comment_id=comment_id)
        GoodCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=GoodCommentManageLog.DELETED)

    def delete_deleted(self, manager_id, comment_id):
        obj = ModerationPenaltyGoodComment.objects.get(moderated_object=self, comment_id=comment_id)
        obj.delete()
        self.delete()
        GoodCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=GoodCommentManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, comment_id):
        self.verified = False
        self.good_comment_moderated_object.all().delete()
        GoodCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=GoodCommentManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, comment_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedGoodComment.STATUS_REJECTED
        GoodCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=GoodCommentManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_good_comment_id=self.pk).all()

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый комментарий к товару'
        verbose_name_plural = 'Проверяемые комментарии к товару'



class GoodModerationReport(models.Model):
    PORNO = 'P'
    NO_CHILD = 'NC'
    BROKEN = 'B'
    FRAUD = 'F'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    ARMS_SALE = 'AS'
    VIOLENCE = 'V'
    PERSECUTION = 'PE'
    SUICIDE = 'SU'
    PETS_ABUSE = 'PA'
    MISREPRESENTATION = "MI"
    EXTREMISM = "EX"
    RHETORIC_HATE = "RH"
    TYPE = (
        (PORNO, 'Порнография'),
        (NO_CHILD, 'Для взрослых'),
        (BROKEN, 'Оскорбительное содержание'),
        (FRAUD, 'Мошенничество'),
        (DRUGS, 'Наркотики'),
        (NO_MORALITY, 'Не нравственный контент'),
        (ARMS_SALE, 'Продажа оружия'),
        (VIOLENCE, 'Насилие'),
        (PERSECUTION, 'Призыв к травле'),
        (SUICIDE, 'Призыв к суициду'),
        (PETS_ABUSE, 'Жестокое обращение c животными'),
        (MISREPRESENTATION, 'Введение в заблуждение'),
        (RHETORIC_HATE, 'Риторика ненависти'),
        (EXTREMISM, 'Экстремизм'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedGood, on_delete=models.CASCADE, related_name='good_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_good_moderation_report(cls, reporter_id, good, description, type):
        moderated_object = ModeratedGood.get_or_create_moderated_object_for_good(good=good)
        good_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return good_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на товар'
        verbose_name_plural = 'Жалобы на товары'

class GoodCommentModerationReport(models.Model):
    PORNO = 'P'
    NO_CHILD = 'NC'
    BROKEN = 'B'
    FRAUD = 'F'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    ARMS_SALE = 'AS'
    VIOLENCE = 'V'
    PERSECUTION = 'PE'
    SUICIDE = 'SU'
    PETS_ABUSE = 'PA'
    MISREPRESENTATION = "MI"
    EXTREMISM = "EX"
    RHETORIC_HATE = "RH"
    TYPE = (
        (PORNO, 'Порнография'),
        (NO_CHILD, 'Для взрослых'),
        (BROKEN, 'Оскорбительное содержание'),
        (FRAUD, 'Мошенничество'),
        (DRUGS, 'Наркотики'),
        (NO_MORALITY, 'Не нравственный контент'),
        (ARMS_SALE, 'Продажа оружия'),
        (VIOLENCE, 'Насилие'),
        (PERSECUTION, 'Призыв к травле'),
        (SUICIDE, 'Призыв к суициду'),
        (PETS_ABUSE, 'Жестокое обращение c животными'),
        (MISREPRESENTATION, 'Введение в заблуждение'),
        (RHETORIC_HATE, 'Риторика ненависти'),
        (EXTREMISM, 'Экстремизм'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_comment_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedGoodComment, on_delete=models.CASCADE, related_name='good_comment_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_good_comment_moderation_report(cls, reporter_id, comment, description, type):
        moderated_object = ModeratedGoodComment.get_or_create_moderated_object_for_comment(comment=comment)
        good_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return good_comment_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на комментрий к товару'
        verbose_name_plural = 'Жалобы на комментрий к товарам'


class ModerationPenaltyGood(models.Model):
    good = models.ForeignKey("goods.Good", on_delete=models.CASCADE, related_name='good_penalties', verbose_name="Оштрафованный товар")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_good_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedGood, on_delete=models.CASCADE, related_name='good_moderated_object', verbose_name="Объект")

    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, good_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, good_id=good_id, type=cls.DELETE)

    def is_deleted(self):
        return self.type == ModerationPenaltyGood.DELETE

    def __str__(self):
        return self.good.creator.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный товар'
        verbose_name_plural = 'Оштрафованные товары'

class ModerationPenaltyGoodComment(models.Model):
    comment = models.ForeignKey("goods.GoodComment", on_delete=models.CASCADE, related_name='good_comment_penalties', verbose_name="Оштрафованный комментарий к товару")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_good_comment_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedGoodComment, on_delete=models.CASCADE, related_name='good_comment_moderated_object', verbose_name="Объект")

    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, comment_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, comment_id=comment_id, type=cls.DELETE)

    def is_deleted(self):
        return self.type == ModerationPenaltyGoodComment.DELETE

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный комментарий к товару'
        verbose_name_plural = 'Оштрафованные комментарии к товарам'
