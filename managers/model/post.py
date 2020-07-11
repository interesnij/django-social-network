from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from managers.models import ModerationCategory
from logs.model.manage_posts import PostManageLog, PostCommentManageLog


class ModeratedPost(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Запись рассматривается'),
        (STATUS_DELETED, 'Запись удалена'),
        (STATUS_REJECTED, 'Запись отвергнута'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='moderated_post', blank=True, verbose_name="Запись")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_moderated_object(cls, post):
        return cls.objects.create(post=post)

    @classmethod
    def _get_or_create_moderated_object(cls, post):
        try:
            moderated_object = cls.objects.get(post=post)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
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
    def is_pending(self):
        # Жалоба рассматривается
        return self.status == ModeratedPost.STATUS_PENDING
    def is_deleted(self):
        # Объект блокирован
        return self.status == ModeratedPost.STATUS_DELETED

    def create_deleted(self, manager_id, post_id):
        self.verified = True
        self.save()
        ModerationPenaltyPost.create_delete_penalty(moderated_object=self, manager_id=manager_id, post_id=post_id)
        PostManageLog.objects.create(post=post_id, manager=manager_id, action_type=PostManageLog.DELETED)

    def delete_deleted(self, manager_id, post_id):
        obj = ModerationPenaltyPost.objects.get(moderated_object=self, post_id=post_id)
        obj.delete()
        self.delete()
        PostManageLog.objects.create(post=post_id, manager=manager_id, action_type=PostManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, post_id):
        self.verified = False
        self.post_moderated_object.all().delete()
        PostManageLog.objects.create(post=post_id, manager=manager_id, action_type=PostManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, post_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedPost.STATUS_REJECTED
        PostManageLog.objects.create(post=post_id, manager=manager_id, action_type=PostManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_post_id=self.pk).all()

    def __str__(self):
        return self.post.creator.get_full_name()

    class Meta:
        verbose_name = 'Проверяемая запись'
        verbose_name_plural = 'Проверяемые записи'


class ModeratedPostComment(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Комментарий рассматривается'),
        (STATUS_DELETED, 'Комментарий удален'),
        (STATUS_REJECTED, 'Комментарий отвергнут'),
    )
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    comment = models.ForeignKey('posts.PostComment', on_delete=models.CASCADE, related_name='moderated_post_comment', blank=True, verbose_name="Комментарий к записи")
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
        return self.post_comment_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedPostComment.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedPostComment.STATUS_DELETED

    def create_deleted(self, manager_id, comment_id):
        self.verified = True
        self.save()
        ModerationPenaltyPostComment.create_delete_penalty(moderated_object=self, manager_id=manager_id, comment_id=comment_id)
        PostCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PostCommentManageLog.DELETED)

    def delete_deleted(self, manager_id, comment_id):
        obj = ModerationPenaltyPostComment.objects.get(moderated_object=self, comment_id=comment_id)
        obj.delete()
        self.delete()
        PostCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PostCommentManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, comment_id):
        self.verified = False
        self.post_comment_moderated_object.all().delete()
        PostCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PostCommentManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, comment_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedPostComment.STATUS_REJECTED
        PostCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PostCommentManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_post_comment_id=self.pk).all()

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый комментарий к записи'
        verbose_name_plural = 'Проверяемые комментарии к записям'



class PostModerationReport(models.Model):
    # жалобы на пользователя.
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

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

class PostCommentModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPostComment, on_delete=models.CASCADE, related_name='post_comment_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_post_comment_moderation_report(cls, reporter_id, comment, description, type):
        moderated_object = ModeratedPostComment.get_or_create_moderated_object_for_comment(comment=comment)
        post_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return post_comment_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на комментрий к записи'
        verbose_name_plural = 'Жалобы на комментрий к записям'


class ModerationPenaltyPost(models.Model):
    # сами санкции против пользователя. Пока только заморозка на разное время.
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='post_penalties', verbose_name="Оштрафованная запись")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_post_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_moderated_object', verbose_name="Объект")

    SUSPENSION = 'S'
    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, post_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, post_id=post_id, type=cls.DELETE)

    def is_deleted(self):
        # Объект блокирован
        return self.type == ModerationPenaltyPost.DELETE

    def __str__(self):
        return self.post.creator.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованная запись'
        verbose_name_plural = 'Оштрафованные записи'

class ModerationPenaltyPostComment(models.Model):
    comment = models.ForeignKey("posts.PostComment", on_delete=models.CASCADE, related_name='post_comment_penalties', verbose_name="Оштрафованный комментарий к записи")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_post_comment_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedPostComment, on_delete=models.CASCADE, related_name='post_moderated_object', verbose_name="Объект")

    SUSPENSION = 'S'
    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, post_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, comment_id=comment_id, type=cls.DELETE)

    def is_deleted(self):
        # Объект блокирован
        return self.type == ModerationPenaltyPostComment.DELETE

    def __str__(self):
        return self.comment.comment.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный комментарий к записи'
        verbose_name_plural = 'Оштрафованные комментарии к записям'
