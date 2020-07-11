from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from logs.model.manage_photo import PhotoManageLog, PhotoCommentManageLog


class ModeratedPhoto(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Фотография рассматривается'),
        (STATUS_DELETED, 'Фотография удалена'),
        (STATUS_REJECTED, 'Фотография отвергнута'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    photo = models.ForeignKey('gallery.Photo', on_delete=models.CASCADE, related_name='moderated_photo', blank=True, verbose_name="Фотография")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_moderated_object(cls, post):
        return cls.objects.create(photo=photo)

    @classmethod
    def _get_or_create_moderated_object(cls, photo):
        try:
            moderated_object = cls.objects.get(photo=photo)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(photo=photo)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_photo(cls, photo):
        return cls._get_or_create_moderated_object(photo=photo)

    @property
    def reports_count(self):
        return self.photo_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedPhoto.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedPhoto.STATUS_DELETED

    def create_deleted(self, manager_id, photo_id):
        self.verified = True
        self.save()
        ModerationPenaltyPhoto.create_delete_penalty(moderated_object=self, manager_id=manager_id, photo_id=photo_id)
        PostManageLog.objects.create(photo=photo_id, manager=manager_id, action_type=PhotoManageLog.DELETED)

    def delete_deleted(self, manager_id, photo_id):
        obj = ModerationPenaltyPhoto.objects.get(moderated_object=self, photo_id=photo_id)
        obj.delete()
        self.delete()
        PhotoManageLog.objects.create(photo=photo_id, manager=manager_id, action_type=PhotoManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, photo_id):
        self.verified = False
        self.photo_moderated_object.all().delete()
        PhotoManageLog.objects.create(photo=photo_id, manager=manager_id, action_type=PhotoManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, photo_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedPhoto.STATUS_REJECTED
        PhotoManageLog.objects.create(photo=photo_id, manager=manager_id, action_type=PhotoManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_photo_id=self.pk).all()

    def __str__(self):
        return self.photo.creator.get_full_name()

    class Meta:
        verbose_name = 'Проверяемая фотография'
        verbose_name_plural = 'Проверяемые фотографии'


class ModeratedPhotoComment(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Фотография рассматривается'),
        (STATUS_DELETED, 'Фотография удалена'),
        (STATUS_REJECTED, 'Фотография отвергнута'),
    )
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, blank=False, null=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    comment = models.ForeignKey('gallery.PhotoComment', on_delete=models.CASCADE, related_name='moderated_photo_comment', blank=True, verbose_name="Комментарий к фотографии")
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
        return self.photo_comment_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedPhotoComment.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedPhotoComment.STATUS_DELETED

    def create_deleted(self, manager_id, comment_id):
        self.verified = True
        self.save()
        ModerationPenaltyPhotoComment.create_delete_penalty(moderated_object=self, manager_id=manager_id, comment_id=comment_id)
        PhotoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PhotoCommentManageLog.DELETED)

    def delete_deleted(self, manager_id, comment_id):
        obj = ModerationPenaltyPhotoComment.objects.get(moderated_object=self, comment_id=comment_id)
        obj.delete()
        self.delete()
        PhotoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PhotoCommentManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, comment_id):
        self.verified = False
        self.photo_comment_moderated_object.all().delete()
        PhotoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PhotoCommentManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, comment_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedPhotoComment.STATUS_REJECTED
        PhotoCommentManageLog.objects.create(comment=comment_id, manager=manager_id, action_type=PhotoCommentManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_photo_comment_id=self.pk).all()

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый комментарий к фотографии'
        verbose_name_plural = 'Проверяемые комментарии к фотографиям'



class PhotoModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPhoto, on_delete=models.CASCADE, related_name='photo_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_photo_moderation_report(cls, reporter_id, photo, description, type):
        moderated_object = ModeratedPhoto.get_or_create_moderated_object_for_post(photo=photo)
        photo_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return photo_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на фотографию'
        verbose_name_plural = 'Жалобы на фотографии'

class PhotoCommentModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_comment_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedPhotoComment, on_delete=models.CASCADE, related_name='photo_comment_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=False, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_photo_comment_moderation_report(cls, reporter_id, comment, description, type):
        moderated_object = ModeratedPhotoComment.get_or_create_moderated_object_for_comment(comment=comment)
        photo_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return photo_comment_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на комментрий к фотографии'
        verbose_name_plural = 'Жалобы на комментрий к фотографиям'


class ModerationPenaltyPhoto(models.Model):
    photo = models.ForeignKey("gallery.Photo", on_delete=models.CASCADE, related_name='photo_penalties', verbose_name="Оштрафованная фотография")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_photo_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedPhoto, on_delete=models.CASCADE, related_name='photo_moderated_object', verbose_name="Объект")

    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, photo_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, photo_id=photo_id, type=cls.DELETE)

    def is_deleted(self):
        return self.type == ModerationPenaltyPhoto.DELETE

    def __str__(self):
        return self.photo.creator.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованная фотография'
        verbose_name_plural = 'Оштрафованные фотографии'

class ModerationPenaltyPhotoComment(models.Model):
    comment = models.ForeignKey("gallery.PhotoComment", on_delete=models.CASCADE, related_name='photo_comment_penalties', verbose_name="Оштрафованный комментарий к фотографии")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_photo_comment_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedPhotoComment, on_delete=models.CASCADE, related_name='post_comment_moderated_object', verbose_name="Объект")

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
        # Объект блокирован
        return self.type == ModerationPenaltyPhotoComment.DELETE

    def __str__(self):
        return self.comment.commenter.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный комментарий к фотографии'
        verbose_name_plural = 'Оштрафованные комментарии к фотографиям'
