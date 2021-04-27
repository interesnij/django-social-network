from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from users.helpers import upload_to_user_directory
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField


class Survey(models.Model):
    PROCESSING = 'PRO'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'
    TIME_END = 'TIM'
    CLOSED = 'CLO'
    MANAGER = 'MAN'
    STATUS = (
        (PROCESSING, 'Обработка'),
        (PUBLISHED, 'Опубликовано'),
        (DELETED, 'Удалено'),
        (TIME_END, 'Время вышло'),
        (CLOSED, 'Закрыто модератором'),
        (MANAGER, 'Созданный персоналом'),
    )
    title = models.CharField(max_length=250, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_creator', verbose_name="Создатель")
    #community = models.ForeignKey('communities.Community', related_name='survey_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    is_anonymous = models.BooleanField(verbose_name="Анонимный", default=False)
    is_multiple = models.BooleanField(verbose_name="Несколько вариантов", default=False)
    is_no_edited = models.BooleanField(verbose_name="Запрет отмены голоса", default=False)
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
    image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 90}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_user_directory)
    status = models.CharField(choices=STATUS, default=PROCESSING, max_length=3)
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title

    @classmethod
    def create_survey(cls, title, community, image, creator, order, is_anonymous, is_multiple, is_no_edited, time_end, answers):
        survey = cls.objects.create(
                                    title=title,
                                    community=community,
                                    image=image,
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
        return SurveyVote.objects.filter(answer__survey_id=self.pk, user_id=user_id).exists()

    def is_time_end(self):
        if self.time_end:
            from datetime import datetime
            now = datetime.now()
            return self.time_end < now:
        else:
            return False

    def get_answers(self):
        return self.survey.only("pk")

    def get_all_count(self):
        count = 0
        for answer in self.get_answers():
            count += answer.get_count()
        if count > 0:
            return count
        else:
            return ''

    def get_votes_count(self):
        query = []
        for answer in self.get_answers():
            query += [answer.get_count()]
        return query

    def get_users(self):
        from users.models import User
        voter_ids = SurveyVote.objects.filter(answer__survey_id=self.pk).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in voter_ids])

    def get_6_users(self):
        from users.models import User
        voter_ids = SurveyVote.objects.filter(answer__survey_id=self.pk).values("user_id")[:6]
        return User.objects.filter(id__in=[i['user_id'] for i in voter_ids])

    def is_have_votes(self):
        return SurveyVote.objects.filter(answer__survey_id=self.pk).values("id").exists()


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
        return SurveyVote.objects.filter(answer_id=self.pk, user_id=user_id).exists()

    def get_answers(self):
        return SurveyVote.objects.filter(answer_id=self.pk)

    def get_procent(self):
        if self.get_count():
            count = self.get_count() / self.survey.get_all_count() * 100
            return int(count)
        else:
            return 0


class SurveyVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='user_voter', verbose_name="Участник опроса")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, db_index=False, related_name='user_answer', verbose_name="Опрос")

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
