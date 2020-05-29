from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings


class QuestionsCategory(models.Model):
	name_ru = models.CharField(max_length=100, unique=True, verbose_name="Русское название")
	name_en = models.CharField(max_length=100, unique=True, verbose_name="Английское название")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	icon = models.CharField(max_length=200, verbose_name="svg icon")

	def __str__(self):
		return self.name_ru

	class Meta:
		verbose_name = "Категория вопросов"
		verbose_name_plural = "Категории вопросов"
		ordering = ['order']


class Question(models.Model):
	quest = models.CharField(max_length=100, unique=True, verbose_name="Вопрос")
	content = RichTextUploadingField(config_name='default',external_plugin_resources=[('youtube','/static/ckeditor_plugins/youtube/youtube/','plugin.js',)],)
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	category = models.ManyToManyField(QuestionsCategory, related_name='questions_categories', verbose_name="Категории вопроса")

	def __str__(self):
		return str(self.order)

	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"
		ordering = ['order']


class QuestionVote(models.Model):
	DONT_LIKE_THIS = 'DL'
	ANSVER_UNCLEAR = 'AU'
	HAVE_QUESTIONS = 'HQ'
	PROBLEM_SOLVED = 'PS'
	VOIS_TYPES = (
	(DONT_LIKE_THIS, 'Мне не нравится, как всё устроено'),
	(ANSVER_UNCLEAR, 'Ответ неясный'),
	(HAVE_QUESTIONS, 'У меня остались вопросы'),
	(PROBLEM_SOLVED, 'Вопрос решен'),
	)
	type = models.CharField(choices=VOIS_TYPES, max_length=2)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='quest_vois', verbose_name="Впрос")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quest_creator', on_delete=models.CASCADE, verbose_name="Создатель")

	def __str__(self):
		return self.type

	class Meta:
		verbose_name = "Голос"
		verbose_name_plural = "Голоса"
