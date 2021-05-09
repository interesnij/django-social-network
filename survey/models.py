import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from users.helpers import upload_to_user_directory
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community


class SurveyList(models.Model):
    MAIN, LIST, MANAGER, THIS_PROCESSING = 'MAI', 'LIS', 'MAN', '_PRO'
    THIS_DELETED, THIS_DELETED_MANAGER = '_DEL', '_DELM'
    THIS_CLOSED, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER, THIS_CLOSED_PRIVATE = '_CLO', '_CLOM', '_CLOMA', '_CLOP'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_surveylist', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_surveylist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип списка")
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список опросов"
        verbose_name_plural = "списки опросов"
        ordering = ['order']

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            SurveyList.objects.create(community=instance, type=SurveyList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            SurveyList.objects.create(creator=instance, type=SurveyList.MAIN, name="Основной список", order=0)

    def is_item_in_list(self, item_id):
        return self.survey_list.filter(pk=item_id).values("pk").exists()

    def is_not_empty(self):
        return self.survey_list.exclude(status__contains="_").values("pk").exists()

    def get_items(self):
        return self.survey_list.filter(status="PUB")
    def get_manager_items(self):
        return self.survey_list.filter(status="MAN")
    def count_items(self):
        return self.survey_list.exclude(status__contains="_").values("pk").count()

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()

    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()

    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] != "_"

    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.survey import get_survey_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="SUL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_survey_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="SUL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_survey_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="SUL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_survey_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="SUL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_survey_list_notify")
        get_survey_list_processing(list, SurveyList.LIST)
        return list
    def edit_list(self, name, description, order, is_public):
        from common.processing.survey import get_survey_list_processing
        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_survey_list_processing(self, SurveyList.LIST)
            self.make_publish()
        else:
            get_survey_list_processing(self, SurveyList.PRIVATE)
            self.make_private()
        return self

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SurveyList.THIS_DELETED
        elif self.type == "MAN":
            self.type = SurveyList.THIS_DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_list(self):
        from notify.models import Notify, Wall
        if self.type == "TDEL":
            self.type = SurveyList.LIST
        elif self.type == "TDELM":
            self.type = SurveyList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SurveyList.THIS_CLOSED
        elif self.type == "MAI":
            self.type = SurveyList.THIS_CLOSED_MAIN
        elif self.type == "MAN":
            self.type = SurveyList.THIS_CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "TCLO":
            self.type = SurveyList.LIST
        elif self.type == "TCLOM":
            self.type = SurveyList.MAIN
        elif self.type == "TCLOM":
            self.type = SurveyList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")


class Survey(models.Model):
    THIS_PROCESSING, MANAGER, PUBLISHED = '_PRO', 'PUB', 'MAN'
    THIS_DELETED, THIS_DELETED_MANAGER = '_DEL', '_DELM'
    THIS_CLOSED, THIS_CLOSED_MANAGER = '_CLO', '_CLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(MANAGER, 'Созданный персоналом'),(PUBLISHED, 'Опубликовано'),
        (THIS_DELETED, 'Удалено'),(THIS_DELETED_MANAGER, 'Удален менеджерский'),
        (THIS_CLOSED, 'Закрыто модератором'),(THIS_CLOSED_MANAGER, 'Закрыт менеджерский'),
    )
    title = models.CharField(max_length=250, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_creator', verbose_name="Создатель")
    is_anonymous = models.BooleanField(verbose_name="Анонимный", default=False)
    is_multiple = models.BooleanField(verbose_name="Несколько вариантов", default=False)
    is_no_edited = models.BooleanField(verbose_name="Запрет отмены голоса", default=False)
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
    image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 90}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_user_directory)
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5)
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания")
    survey = models.ForeignKey(SurveyList, on_delete=models.CASCADE, related_name='survey_list', verbose_name="Список")
    community = models.ForeignKey('communities.Community', related_name='survey_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    vote = models.PositiveIntegerField(default=0, verbose_name="Кол-во голосов")
    voter = models.PositiveIntegerField(default=0, verbose_name="Кол-во людей")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title

    def plus_reposts(self, count):
        self.repost += count
        return self.save(update_fields=['repost'])
    def minus_reposts(self, count):
        self.repost -= count
        return self.save(update_fields=['repost'])
    def plus_votes(self, count):
        self.vote += count
        return self.save(update_fields=['vote'])
    def minus_votes(self, count):
        self.vote -= count
        return self.save(update_fields=['vote'])
    def plus_voters(self, count):
        self.voter += count
        return self.save(update_fields=['voter'])
    def minus_voters(self, count):
        self.voter -= count
        return self.save(update_fields=['voter'])

    @classmethod
    def create_survey(cls, title, image, lists, creator, order, is_anonymous, is_multiple, is_no_edited, time_end, answers, community):
        from common.processing.survey import get_survey_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")

        survey = cls.objects.create(title=title,image=image,creator=creator,order=order,is_anonymous=is_anonymous,is_multiple=is_multiple,is_no_edited=is_no_edited,time_end=time_end)
        for answer in answers:
            Answer.objects.create(survey=survey, text=answer)
        for list_id in lists:
            list = SurveyList.objects.get(pk=list_id)
            list.survey_list.add(survey)
        get_survey_processing(survey, Survey.PUBLISHED)
        if community:
            from common.notify.progs import community_send_notify, community_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="SUR", object_id=survey.pk, verb="ITE")
            community_send_wall(doc.pk, creator.pk, community.pk, None, "create_c_survey_wall")
            for user_id in community.get_member_for_notify_ids():
                Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="SUR", object_id=survey.pk, verb="ITE")
                community_send_notify(doc.pk, creator.pk, user_id, community.pk, None, "create_c_survey_notify")
        else:
            from common.notify.progs import user_send_notify, user_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, type="SUR", object_id=survey.pk, verb="ITE")
            user_send_wall(survey.pk, None, "create_u_survey_wall")
            for user_id in creator.get_user_news_notify_ids():
                Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="SUR", object_id=survey.pk, verb="ITE")
                user_send_notify(survey.pk, creator.pk, user_id, None, "create_u_survey_notify")
        return survey

    def edit_survey(self, title, image, lists, order, is_anonymous, is_multiple, is_no_edited, time_end, answers):
        from common.processing.survey  import get_survey_processing

        get_survey_processing(self, Survey.PUBLISHED)
        self.title = title
        self.image = image
        self.lists = lists
        self.order = order
        self.is_anonymous = is_anonymous
        self.is_multiple = is_multiple
        self.is_no_edited = is_no_edited
        self.time_end = time_end
        self.save()
        if set(answers) != set(self.get_answers()):
            self.survey.all().delete()
            for answer in answers:
                Answer.objects.create(survey=survey, text=answer)
        return survey

    def is_user_voted(self, user_id):
        return SurveyVote.objects.filter(answer__survey_id=self.pk, user_id=user_id).exists()

    def is_time_end(self):
        if self.time_end:
            from datetime import datetime
            now = datetime.now()
            return self.time_end < now
        else:
            return False

    def get_answers(self):
        return self.survey.only("text")

    def get_all_count(self):
        if self.vote > 0:
            return self.vote

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

    def delete_survey(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Survey.THIS_DELETED
        elif self.status == "MAN":
            self.status = Survey.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
    def restore_survey(self):
        from notify.models import Notify, Wall
        if self.status == "TDEL":
            self.status = Survey.PUBLISHED
        elif self.status == "TDELM":
            self.status = Survey.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Survey.THIS_CLOSED
        elif self.status == "MAN":
            self.status = Survey.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.status == "TCLO":
            self.status = Survey.PUBLISHED
        elif self.status == "TCLOM":
            self.status = Survey.MANAGER
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")


class Answer(models.Model):
    text = models.CharField(max_length=250, verbose_name="Вариант ответа")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='+', verbose_name="Опрос")
    vote = models.PositiveIntegerField(default=0, verbose_name="Кол-во голосов")

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.text

    def get_count(self):
        return self.vote

    def is_user_voted(self, user_id):
        return SurveyVote.objects.filter(answer_id=self.pk, user_id=user_id).exists()

    def get_answers(self):
        return SurveyVote.objects.filter(answer_id=self.pk)

    def get_procent(self):
        if self.vote:
            count = self.vote / self.survey.vote * 100
            return int(count)
        else:
            return 0

    def plus_votes(self, count):
        self.vote += count
        return self.save(update_fields=['vote'])
    def minus_votes(self, count):
        self.vote -= count
        return self.save(update_fields=['vote'])

    def vote(self, user, community):
        import json
        from datetime import datetime
        from django.http import HttpResponse

        survey = self.survey
        if survey.time_end < datetime.now():
            pass
        try:
            answer = SurveyVote.objects.get(answer=answer, user_id=user.pk)
            if survey.is_no_edited:
                pass
            else:
                answer.delete()
        except SurveyVote.DoesNotExist:
            if not survey.is_multiple and user.is_voted_of_survey(survey.pk):
                user.get_vote_of_survey(survey.pk).delete()
            SurveyVote.objects.create(answer=answer, user=user.user)
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, survey.pk, "SUR", "c_survey_vote_notify", "SVO")
                community_wall(user, community, None, survey.pk, "SUR", "c_survey_vote_wall", "SVO")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, survey.pk, "SUR", "u_survey_vote_notify", "SVO")
                user_wall(user, None, survey.pk, "SUR", "u_survey_vote_wall", "SVO")
        return HttpResponse(json.dumps({"votes": survey.get_votes_count()}), content_type="application/json")


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
