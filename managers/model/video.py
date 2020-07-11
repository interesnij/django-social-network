from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from logs.model.manage_video import VideoManageLog, VideoCommentManageLog


class ModeratedVideo(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Ролик рассматривается'),
        (STATUS_DELETED, 'Ролик удален'),
        (STATUS_REJECTED, 'Ролик отвергнут'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, related_name='moderated_video', blank=True, verbose_name="Ролик")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_moderated_object(cls, video):
        return cls.objects.create(video=video)

    @classmethod
    def _get_or_create_moderated_object(cls, video):
        try:
            moderated_object = cls.objects.get(video=video)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(video=video)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_video(cls, video):
        return cls._get_or_create_moderated_object(video=video)

    @property
    def reports_count(self):
        return self.video_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedVideo.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedVideo.STATUS_DELETED

    def create_deleted(self, manager_id, video_id):
        self.verified = True
        self.save()
        ModerationPenaltyVideo.create_delete_penalty(moderated_object=self, manager_id=manager_id, video_id=video_id)
        VideoManageLog.objects.create(video=video_id, manager=manager_id, action_type=VideoManageLog.DELETED)

    def delete_deleted(self, manager_id, video_id):
        obj = ModerationPenaltyVideo.objects.get(moderated_object=self, video_id=video_id)
        obj.delete()
        self.delete()
        VideoManageLog.objects.create(video=video_id, manager=manager_id, action_type=VideoManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, video_id):
        self.verified = False
        self.video_moderated_object.all().delete()
        VideoManageLog.objects.create(video=video_id, manager=manager_id, action_type=VideoManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, video_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedVideo.STATUS_REJECTED
        VideoManageLog.objects.create(video=video_id, manager=manager_id, action_type=VideoManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_video_id=self.pk).all()

    def __str__(self):
        return self.video.creator.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый ролик'
        verbose_name_plural = 'Проверяемые ролики'


class ModeratedVideoComment(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Ролик рассматривается'),
        (STATUS_DELETED, 'Ролик удален'),
        (STATUS_REJECTED, 'Ролик отвергнут'),
    )
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    comment = models.ForeignKey('video.VideoComment', on_delete=models.CASCADE, related_name='moderated_video_comment', blank=True, verbose_name="Комментарий к ролику")
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
        return self.video_comment_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedVideoComment.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedVideoComment.STATUS_DELETED

    def create_deleted(self, manager_id, comment_id):
        self.verified = True
        self.save()
        ModerationPenaltyVideoComment.create_delete_penalty(moderated_object=self, manager_id=manager_id, comment_id=comment_id)
        VideoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=VideoCommentManageLog.DELETED)

    def delete_deleted(self, manager_id, comment_id):
        obj = ModerationPenaltyVideoComment.objects.get(moderated_object=self, comment_id=comment_id)
        obj.delete()
        self.delete()
        VideoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=VideoCommentManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, comment_id):
        self.verified = False
        self.video_comment_moderated_object.all().delete()
        VideoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=VideoCommentManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, comment_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedVideoComment.STATUS_REJECTED
        VideoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=VideoCommentManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_video_comment_id=self.pk).all()

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый комментарий к ролику'
        verbose_name_plural = 'Проверяемые комментарии к роликам'



class VideoModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedVideo, on_delete=models.CASCADE, related_name='video_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_photo_moderation_report(cls, reporter_id, video, description, type):
        moderated_object = ModeratedVideo.get_or_create_moderated_object_for_video(video=video)
        video_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return video_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на ролик'
        verbose_name_plural = 'Жалобы на ролики'

class VideoCommentModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_comment_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedVideoComment, on_delete=models.CASCADE, related_name='video_comment_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_video_comment_moderation_report(cls, reporter_id, comment, description, type):
        moderated_object = ModeratedVideoComment.get_or_create_moderated_object_for_comment(comment=comment)
        video_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return video_comment_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на комментрий к ролику'
        verbose_name_plural = 'Жалобы на комментрий к роликам'


class ModerationPenaltyVideo(models.Model):
    video = models.ForeignKey("video.Video", on_delete=models.CASCADE, related_name='video_penalties', verbose_name="Оштрафованный ролик")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_video_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedVideo, on_delete=models.CASCADE, related_name='video_moderated_object', verbose_name="Объект")

    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, video_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, video_id=video_id, type=cls.DELETE)

    def is_deleted(self):
        return self.type == ModerationPenaltyVideo.DELETE

    def __str__(self):
        return self.video.creator.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный ролик'
        verbose_name_plural = 'Оштрафованные ролики'

class ModerationPenaltyVideoComment(models.Model):
    comment = models.ForeignKey("video.VideoComment", on_delete=models.CASCADE, related_name='video_comment_penalties', verbose_name="Оштрафованный комментарий к ролику")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_video_comment_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedVideoComment, on_delete=models.CASCADE, related_name='video_comment_moderated_object', verbose_name="Объект")

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
        return self.type == ModerationPenaltyVideoComment.DELETE

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный комментарий к ролику'
        verbose_name_plural = 'Оштрафованные комментарии к роликам'
