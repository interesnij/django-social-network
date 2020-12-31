from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex


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
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

    post = models.ManyToManyField("posts.Post", blank=True, related_name='post_survey')

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title

    @classmethod
    def create_survey(cls, title, community, creator, order, is_anonymous, is_multiple, is_no_edited, time_end, answers):
        survey = cls.objects.create(
                                    title=title,
                                    community=community,
                                    creator=creator,
                                    order=order,
                                    is_anonymous=is_anonymous,
                                    is_multiple=is_multiple,
                                    is_no_edited=is_no_edited,
                                    time_end=time_end)
        for answer in answers:
            Answer.objects.create(survey=survey, text=answer)
        return survey

    def is_user_voted(self, user_id):
        return self.survey.filter(survey__user_voter_id=user_id).exists()

    def get_answers(self):
        return self.survey.only("pk")

    def get_all_count(self):
        count = 0
        for answer in self.get_answers():
            count += answer.get_count()
        return count

    def get_votes_count(self):
        query = []
        for answer in self.get_answers():
            query += [answer.get_count()]
        return query

    def get_users(self):
        from users.models import User
        voter_ids = SurveyVote.objects.filter(answer__survey_id=self.pk).values("user_id")
        ids = [i['user_id'] for i in voter_ids]
        return User.objects.get(id__in=ids)


class Answer(models.Model):
    text = models.CharField(max_length=250, verbose_name="Вариант ответа")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey', verbose_name="Опрос")

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.text

    def get_count(self):
        return self.user_answer.all().values("pk").count()

    def is_user_voted(self, user_id):
        return self.user_voter.filter(answer_id=self.pk, user_id=user_id).exists()

    def get_answers(self):
        return SurveyVote.objects.filter(answer_id=self.pk)

    def get_procent(self):
        return self.get_count() * 100 / self.survey.get_all_count()


class SurveyVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_voter', verbose_name="Участник опроса")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='user_answer', verbose_name="Опрос")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_answer(cls, user, answer):
        return cls.objects.create(user=user, answer=answer)

    class Meta:
        unique_together = (('user', 'answer'),)
        indexes = [
            models.Index(fields=['answer', 'user']),
            ]
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
