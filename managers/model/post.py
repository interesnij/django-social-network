from django.conf import settings
from django.db import models
from django.utils import timezone
from posts.models import Post, PostComment
from managers.models import ModerationCategory


class ModeratedPost(models.Model):
    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобренный'),
        (STATUS_REJECTED, 'Отвергнутый'),
    )
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Одобрено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    category = models.ForeignKey(ModerationCategory, blank=True, on_delete=models.CASCADE, related_name='moderated_post', verbose_name="Категория")
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, blank=True, verbose_name="Запись")
    post_comment = models.ForeignKey("posts.PostComment", on_delete=models.CASCADE, blank=True, verbose_name="Запись")

    @classmethod
    def create_moderated_object(cls, post, post_comment):
        return cls.objects.create(post=post, post_comment=post_comment)

    @classmethod
    def _get_or_create_moderated_object(cls, post, post_comment):
        try:
            moderated_object = cls.objects.get(post=post, post_comment=post_comment)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(post=post, post_comment=post_comment)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_post(cls, post):
        return cls._get_or_create_moderated_object(post=post)

    @classmethod
    def get_or_create_moderated_object_for_post_comment(cls, post_comment):
        return cls._get_or_create_moderated_object(post_comment=post_comment)

    @property
    def reports_count(self):
        return self.post_reports.count()

    def is_verified(self):
        return self.verified

    def is_approved(self):
        return self.status == ModeratedPost.STATUS_APPROVED

    def is_pending(self):
        return self.status == ModeratedPost.STATUS_PENDING

    def update_with_actor_with_id(self, description, category_id):
        current_description = self.description
        self.description = description
        current_category_id = self.category_id
        self.category_id = category_id
        self.save()

    def verify_with_actor_with_id(self, severity):
        current_verified = self.verified
        self.verified = True
        moderation_severity = severity
        penalty_targets = None

        if self.is_approved():
            if isinstance(self.post, Post):
                penalty_targets = [self.post.creator]
            elif isinstance(self.post_comment, PostComment):
                penalty_targets = [self.post_comment.commenter]
            for penalty_target in penalty_targets:
                duration_of_penalty = None
                penalties_count = penalty_target.count_post_penalties_for_moderation_severity(moderation_severity=moderation_severity) + 1

                if moderation_severity == ModerationCategory.SEVERITY_CRITICAL:
                    duration_of_penalty = timezone.timedelta(weeks=5000)
                elif moderation_severity == ModerationCategory.SEVERITY_HIGH:
                    duration_of_penalty = timezone.timedelta(days=penalties_count ** 4)
                elif moderation_severity == ModerationCategory.SEVERITY_MEDIUM:
                    duration_of_penalty = timezone.timedelta(hours=penalties_count ** 3)
                elif moderation_severity == ModerationCategory.SEVERITY_LOW:
                    duration_of_penalty = timezone.timedelta(minutes=penalties_count ** 2)
                moderation_expiration = timezone.now() + duration_of_penalty
                ModerationPenaltyPost.create_suspension_moderation_penalty(moderated_object=self, user_id=penalty_target.pk, expiration=moderation_expiration)
        self.save()

    def unverify_with_actor_with_id(self):
        current_verified = self.verified
        self.verified = False
        self.post_penalties.all().delete()
        moderation_severity = severity
        self.save()

    def approve_with_actor_with_id(self):
        current_status = self.status
        self.status = ModeratedPost.STATUS_APPROVED
        self.save()

    def reject_with_actor_with_id(self):
        current_status = self.status
        self.status = ModeratedPost.STATUS_REJECTED
        self.save()

    def get_reporters(self):
        return User.objects.filter(post_reports__moderated_post_id=self.pk).all()


class PostModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True,verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")

    @classmethod
    def create_post_moderation_report(cls, reporter_id, post, description):
        moderated_object = ModeratedPost.get_or_create_moderated_object_for_post(post=post, category_id=category_id)
        post_moderation_report = cls.objects.create(reporter_id=reporter_id, description=description, moderated_object=moderated_object)
        return post_moderation_report

    @classmethod
    def create_post_comment_moderation_report(cls, reporter_id, post_comment, description):
        moderated_object = ModeratedPost.get_or_create_moderated_object_for_post_comment(post_comment=post_comment, category_id=category_id)
        post_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, description=description, moderated_object=moderated_object)
        return post_comment_moderation_report


class ModerationPenaltyPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_penalties', verbose_name="Оштрафованный пользователь")
    expiration = models.DateTimeField(null=True,verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_penalties', verbose_name="Объект")

    TYPE_SUSPENSION = 'S'
    TYPE_DELETED = 'D'
    TYPE_BANNER = 'D'
    TYPES = (
        (TYPE_SUSPENSION, 'Приостановлено'),
    )
    type = models.CharField(max_length=5, choices=TYPES,verbose_name="Тип")

    @classmethod
    def create_suspension_moderation_penalty(cls, user_id, moderated_object, expiration):
        return cls.objects.create(moderated_object=moderated_object, user_id=user_id, type=cls.TYPE_SUSPENSION, expiration=expiration)
