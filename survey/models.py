from django.db import models
from django.utils import timezone
from django.conf import settings


class Survey(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_creator', verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='survey_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)
    is_anonymous = models.BooleanField(verbose_name="Анонимный", default=False)
    is_multiple = models.BooleanField(verbose_name="Несколько вариантов", default=False)
    is_no_edited = models.BooleanField(verbose_name="Запрет отмены голоса", default=False)
    time_end = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name="Дата окончания")

    post = models.ManyToManyField("posts.Post", blank=True, related_name='post_survey')

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title

    @classmethod
    def create_survey(cls, title, community, creator, is_deleted, is_anonymous, is_multiple, is_no_edited, time_end, answers):
        survey = cls.objects.create(
                                    title=title,
                                    community=community,
                                    creator=creator,
                                    is_deleted=is_deleted,
                                    is_anonymous=is_anonymous,
                                    is_multiple=is_multiple,
                                    is_no_edited=is_no_edited,
                                    time_end=time_end)
        SurveyMembership.create_membership(user=creator, survey=survey)
        for answer in answers:
            Answer.objects.create(survey=survey, text=answer)
        return survey


class Answer(models.Model):
    text = models.CharField(max_length=250, verbose_name="Вариант ответа")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey', verbose_name="Опрос")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.text


class SurveyMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='survey_memberships', null=False, blank=False, verbose_name="Участник опроса")
    survey = models.ForeignKey(Survey, db_index=False, on_delete=models.CASCADE, related_name='surveys', null=False, blank=False, verbose_name="Опрос")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_membership(cls, user, survey):
        return cls.objects.create(user=user, survey=survey)

    class Meta:
        unique_together = (('user', 'survey'),)
        indexes = [
            models.Index(fields=['survey', 'user']),
            ]
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
