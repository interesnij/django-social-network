from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import User
from logs.model.manage_audio import AudioManageLog


class ModeratedAudio(models.Model):
    STATUS_PENDING = 'P'
    STATUS_DELETED = 'D'
    STATUS_REJECTED = 'R'
    STATUSES = (
        (STATUS_PENDING, 'Трек рассматривается'),
        (STATUS_DELETED, 'Трек удален'),
        (STATUS_REJECTED, 'Трек отвергнут'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")
    good = models.ForeignKey('music.SoundcloudParsing', on_delete=models.CASCADE, related_name='moderated_audio', blank=True, verbose_name="Товар")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_moderated_object(cls, audio):
        return cls.objects.create(audio=audio)

    @classmethod
    def _get_or_create_moderated_object(cls, audio):
        try:
            moderated_object = cls.objects.get(audio=audio)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(audio=audio)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_audio(cls, audio):
        return cls._get_or_create_moderated_object(audio=audio)

    @property
    def reports_count(self):
        return self.audio_reports.count()

    def is_verified(self):
        return self.verified
    def is_pending(self):
        return self.status == ModeratedAudio.STATUS_PENDING
    def is_deleted(self):
        return self.status == ModeratedAudio.STATUS_DELETED

    def create_deleted(self, manager_id, good_id):
        self.verified = True
        self.save()
        ModerationPenaltyAudio.create_delete_penalty(moderated_object=self, manager_id=manager_id, audio_id=audio_id)
        AudioManageLog.objects.create(audio=audio_id, manager=manager_id, action_type=AudioManageLog.DELETED)

    def delete_deleted(self, manager_id, audio_id):
        obj = ModerationPenaltyAudio.objects.get(moderated_object=self, audio_id=audio_id)
        obj.delete()
        self.delete()
        AudioManageLog.objects.create(audio=audio_id, manager=manager_id, action_type=AudioManageLog.UNDELETED)

    def unverify_moderation(self, manager_id, audio_id):
        self.verified = False
        self.audio_moderated_object.all().delete()
        AudioManageLog.objects.create(audio=audio_id, manager=manager_id, action_type=AudioManageLog.UNVERIFY)
        self.save()

    def reject_moderation(self, manager_id, audio_id):
        self.verified = True
        current_status = self.status
        self.status = ModeratedAudio.STATUS_REJECTED
        AudioManageLog.objects.create(audio=audio_id, manager=manager_id, action_type=AudioManageLog.REJECT)
        self.save()

    def get_reporters(self):
        return User.objects.filter(user_reports__moderated_audio_id=self.pk).all()

    def __str__(self):
        return self.audio.creator.get_full_name()

    class Meta:
        verbose_name = 'Проверяемый трек'
        verbose_name_plural = 'Проверяемые треки'


class AudioModerationReport(models.Model):
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

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='audio_reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedAudio, on_delete=models.CASCADE, related_name='audio_reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, null=True, verbose_name="Описание")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип нарушения")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_audio_moderation_report(cls, reporter_id, audio, description, type):
        moderated_object = ModeratedAudio.get_or_create_moderated_object_for_audio(audio=adio)
        audio_moderation_report = cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)
        return audio_moderation_report

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на трек'
        verbose_name_plural = 'Жалобы на треки'


class ModerationPenaltyAudio(models.Model):
    audio = models.ForeignKey("music.SoundcloudParsing", on_delete=models.CASCADE, related_name='audio_penalties', verbose_name="Оштрафованный трек")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_audio_penalties', verbose_name="Менеджер")
    moderated_object = models.ForeignKey(ModeratedAudio, on_delete=models.CASCADE, related_name='audio_moderated_object', verbose_name="Объект")

    DELETE = 'D'
    TYPES = (
        (DELETE, 'Удалено'),
    )
    type = models.CharField(max_length=5, choices=TYPES, verbose_name="Тип")
    id = models.BigAutoField(primary_key=True)

    @classmethod
    def create_delete_penalty(cls, audio_id, manager_id, moderated_object):
        return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, audio_id=audio_id, type=cls.DELETE)

    def is_deleted(self):
        return self.type == ModerationPenaltyAudio.DELETE

    def __str__(self):
        return self.audio.creator.get_full_name()

    class Meta:
        verbose_name = 'Оштрафованный трек'
        verbose_name_plural = 'Оштрафованные треки'
