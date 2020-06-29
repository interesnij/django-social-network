from django.conf import settings
from django.db import models
from django.utils import timezone
from posts.models import Post, PostComment
from moderation.models import ModerationCategory


class ModeratedPost(models.Model):
    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобренный'),
        (STATUS_REJECTED, 'Отвергнутый'),
    )
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Одобрено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    category = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='moderated_post', verbose_name="Категория")
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, blank=True, verbose_name="Запись")
    post_comment = models.ForeignKey("posts.PostComment", on_delete=models.CASCADE, blank=True, verbose_name="Запись")

    @classmethod
    def create_moderated_object(cls, post, post_comment, category_id):
        return cls.objects.create(post=post, post_comment=post_comment, category_id=category_id)

    @classmethod
    def _get_or_create_moderated_object(cls, post, post_comment, category_id):
        try:
            moderated_object = cls.objects.get(post=post, post_comment=post_comment, object_id=post.pk)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(post=post, post_comment=post_comment, category_id=category_id)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_post(cls, post, category_id):
        community_id = None
        if post.community:
            community_id = post.community.pk
        return cls._get_or_create_moderated_object(post=post, category_id=category_id)

    @classmethod
    def get_or_create_moderated_object_for_post_comment(cls, post_comment, category_id):
        community_id = None
        if post_comment.post.community:
            community_id = post_comment.post.community.pk
        return cls._get_or_create_moderated_object(post_comment=post_comment, category_id=category_id, community_id=community_id)

    @property
    def reports_count(self):
        return self.reports.count()

    def is_verified(self):
        return self.verified

    def is_approved(self):
        return self.status == ModeratedPost.STATUS_APPROVED

    def is_pending(self):
        return self.status == ModeratedPost.STATUS_PENDING

    def update_with_actor_with_id(self, actor_id, description, category_id):
        if description is not None:
            current_description = self.description
            self.description = description

        if category_id is not None:
            current_category_id = self.category_id
            self.category_id = category_id
        self.save()

    def verify_with_actor_with_id(self, actor_id):
        current_verified = self.verified
        self.verified = True
        moderation_severity = self.category.severity
        penalty_targets = None

        if self.is_approved():
            if isinstance(self.post, Post):
                penalty_targets = [self.post.creator]
            elif isinstance(self.post_comment, PostComment):
                penalty_targets = [self.post_comment.commenter]
            for penalty_target in penalty_targets:
                duration_of_penalty = None
                penalties_count = penalty_target.count_moderation_penalties_for_moderation_severity(
                    moderation_severity=moderation_severity) + 1

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

    def unverify_with_actor_with_id(self, actor_id):
        current_verified = self.verified
        self.verified = False
        self.user_penalties.all().delete()
        moderation_severity = self.category.severity
        self.save()

    def approve_with_actor_with_id(self, actor_id):
        current_status = self.status
        self.status = ModeratedPost.STATUS_APPROVED
        self.save()

    def reject_with_actor_with_id(self, actor_id):
        current_status = self.status
        self.status = ModeratedPost.STATUS_REJECTED
        self.save()

    def get_reporters(self):
        return User.objects.filter(post_reports__moderated_object_id=self.pk).all()


class PostModerationReport(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Объект")
    category = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='post_reports', null=False, verbose_name="Категория")
    description = models.CharField(max_length=300, blank=False, null=True,verbose_name="Описание")

    @classmethod
    def create_post_moderation_report(cls, reporter_id, post, category_id, description):
        moderated_object = ModeratedPost.get_or_create_moderated_object_for_post(post=post, category_id=category_id)
        post_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id, description=description, moderated_object=moderated_object)
        return post_moderation_report

    @classmethod
    def create_post_comment_moderation_report(cls, reporter_id, post_comment, category_id, description):
        moderated_object = ModeratedPost.get_or_create_moderated_object_for_post_comment(post_comment=post_comment, category_id=category_id)
        post_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id, description=description, moderated_object=moderated_object)
        return post_comment_moderation_report


class ModerationPenaltyPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_penalties', verbose_name="Оштрафованный пользователь")
    expiration = models.DateTimeField(null=True,verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedPost, on_delete=models.CASCADE, related_name='post_penalties', verbose_name="Объект")

    TYPE_SUSPENSION = 'S'
    TYPES = (
        (TYPE_SUSPENSION, 'Приостановлено'),
    )
    type = models.CharField(max_length=5, choices=TYPES,verbose_name="Тип")

    @classmethod
    def create_suspension_moderation_penalty(cls, user_id, moderated_object, expiration):
        return cls.objects.create(moderated_object=moderated_object, user_id=user_id, type=cls.TYPE_SUSPENSION, expiration=expiration)
