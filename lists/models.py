from django.db import models
from django.db.models import Q
from django.conf import settings
import uuid


class AuthorityListCategory(models.Model):
	name = models.CharField(max_length=100,verbose_name="Название категории блога")
	order = models.PositiveSmallIntegerField(default=0,verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Категория органа власти"
		verbose_name_plural = "Категории органов власти"

	def get_lists(self):
		return AuthorityList.objects.filter(category=self)


class AuthorityList(models.Model):
	name = models.CharField(max_length=100, verbose_name="Список депутатов")
	slug = models.CharField(max_length=100, verbose_name="Англ. название для списка")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	is_reginal = models.BooleanField(default=True, verbose_name="Региональный список")
	is_in_left_menu = models.BooleanField(default=False, verbose_name="Выводится в левом меню")
	is_active = models.BooleanField(default=False, verbose_name="Действующий список")
	category = models.ForeignKey(AuthorityListCategory, on_delete=models.CASCADE, related_name="+", blank=True, null=True, verbose_name="Категория органа власти")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Список депутатов"
		verbose_name_plural = "Списки депутатов"

	def __str__(self):
		return self.name

	def is_list_not_empty(self):
		return AuthorityList.objects.filter(category_id=self.pk).exists()

	def get_elects(self):
		from elect.models import Elect
		return Elect.objects.filter(list=self)

	def get_elects_10(self):
		from elect.models import Elect
		return Elect.objects.filter(list=self)[:10]


class ElectNewsCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название категории новостей о депутате")
	slug = models.CharField(max_length=100, verbose_name="Англ. название для категории")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "категория активностей"
		verbose_name_plural = "категория активностей"


class BlogCategory(models.Model):
	name = models.CharField(max_length=100,verbose_name="Название категории блога")
	slug = models.CharField(max_length=100,verbose_name="Англ. название для ссылки")
	order = models.PositiveSmallIntegerField(default=0,verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "категория блога"
		verbose_name_plural = "категории блога"

	def is_article_exists(self):
		return self.blog_categories.filter(category=self).values("pk").exists()

	def get_articles_10(self):
		return self.blog_categories.filter(category=self)[:10]

	def get_articles(self):
		return self.blog_categories.filter(category=self)

class Fraction(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название фракции")
	slug = models.CharField(blank=True, max_length=100, verbose_name="Для ссылки английское название")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Фракция"
		verbose_name_plural = "Фракции"

	def get_elects(self):
		from elect.models import Elect
		return Elect.objects.filter(fraction=self)


class MediaList(models.Model):
	LIST = 'LIS'
	DELETED = '_DEL'
	TYPE = (
		(LIST, 'Основной'),
		(DELETED, 'Удалённый'),
	)

	name = models.CharField(max_length=255)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_medialist', on_delete=models.CASCADE, verbose_name="Создатель")
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_medialist', on_delete=models.CASCADE, verbose_name="Владелец")
	order = models.PositiveIntegerField(default=1)
	uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
	description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
	type = models.CharField(max_length=4, choices=TYPE, default=LIST, verbose_name="Тип листа")

	def __str__(self):
		return self.name + " " + self.creator.get_full_name()

	class Meta:
		verbose_name = "медийный список"
		verbose_name_plural = "медийные списки"
		ordering = ['order']

	@classmethod
	def create_list(cls, creator, name, description, order):
		from common.processing import get_media_list_processing
		if not order:
			order = 1

		list = cls.objects.create(creator=creator,name=name,description=description,order=order)
		get_media_list_processing(list, MediaList.LIST)
		return list

	def edit_list(self, name, description, order):
		from common.processing import get_media_list_processing

		if not order:
			order = 1
		self.name = name
		self.description = description
		self.order = order
		self.save()
		get_media_list_processing(self, MediaList.LIST)
		return self

	def is_item_in_list(self, item_id):
		return self.media_list.filter(type="PUB").exists()

	def is_not_empty(self):
		return self.media_list.filter(type="PUB").values("pk").exists()

	def get_items(self):
		return self.media_list.filter(type="PUB")

	def count_items(self):
		return self.media_list.filter(Q(type="PUB")|Q(type="PRI")).values("pk").count()

	def is_deleted(self):
		return self.type == "_DEL"

	def delete_list(self):
		from notify.models import Notify, Wall
		self.type = MediaList.DELETED
		self.save(update_fields=['type'])

	def abort_delete_list(self):
		from notify.models import Notify, Wall
		self.type = MediaList.LIST
		self.save(update_fields=['type'])
