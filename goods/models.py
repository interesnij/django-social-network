from django.db import models
import uuid
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from django.db.models import Q
from goods.helpers import upload_to_good_directory
from django.db.models.signals import post_save
from django.dispatch import receiver


class GoodCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название категории")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
	image = models.ImageField(blank=True, verbose_name="Изображение", upload_to="goods/list")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order","name"]
		verbose_name = "категория товаров"
		verbose_name_plural = "категории товаров"


class GoodSubCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название подкатегории")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер подкатегории")
	category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE, verbose_name="Категория-родитель")
	image = models.ImageField(blank=True, verbose_name="Изображение", upload_to="goods/list")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order","name"]
		verbose_name = "Подкатегория товаров"
		verbose_name_plural = "Подкатегории товаров"


class GoodList(models.Model):
	MAIN, LIST, MANAGER, THIS_PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', 'TPRO', 'PRI'
	THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = 'TDEL', 'TDELP', 'TDELM'
	THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER = 'TCLO', 'TCLOP', 'TCLOM', 'TCLOMA'
	TYPE = (
		(MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),
		(THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
		(THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
		)
	community = models.ForeignKey('communities.Community', related_name='good_lists_community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
	uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
	name = models.CharField(max_length=250, verbose_name="Название")
	type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип альбома")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	order = models.PositiveIntegerField(default=0)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_list_creator', verbose_name="Создатель")
	description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

	users = models.ManyToManyField("users.User", blank=True, related_name='+')
	communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name = 'Подборка товаров'
		verbose_name_plural = 'Подборки товаров'

	def __str__(self):
		return self.title

	#@receiver(post_save, sender=settings.COMMUNITY_MODEL)
	def create_c_model(sender, instance, created, **kwargs):
		if created:
			community=instance
			GoodList.objects.create(community=community, type=GoodList.MAIN, name="Основной список", order=0, creator=community.creator)
	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_u_model(sender, instance, created, **kwargs):
		if created:
			GoodList.objects.create(creator=instance, type=GoodList.MAIN, name="Основной список", order=0)

	def is_main(self):
		return self.type == self.MAIN
	def is_list(self):
		return self.type == self.LIST
	def is_private(self):
		return self.type == self.PRIVATE
	def is_open(self):
		return self.type[0] != "T"

	def get_items(self):
		return self.good_list.filter(status="PUB")
	def get_staff_items(self):
		return self.good_list.filter(Q(status="PUB")|Q(status="PRI"))
	def count_items(self):
		try:
			return self.good_list.filter(status="PUB").values("pk").count()
		except:
			return 0
	def count_items_ru(self):
		count = self.count_items()
		a, b = count % 10, count % 100
		if (a == 1) and (b != 11):
			return str(count) + " товар"
		elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
			return str(count) + " товара"
		else:
			return str(count) + " товаров"

	def is_not_empty(self):
		 return self.good_list.filter(status="PUB").values("pk").exists()
	def get_users_ids(self):
		users = self.users.exclude(type__contains="THIS").values("pk")
		return [i['pk'] for i in users]
	def get_communities_ids(self):
		communities = self.communities.exclude(type__contains="THIS").values("pk")
		return [i['pk'] for i in communities]

	def is_user_can_add_list(self, user_id):
		return self.creator.pk != user_id and user_id not in self.get_users_ids()
	def is_user_can_delete_list(self, user_id):
		return self.creator.pk != user_id and user_id in self.get_users_ids()

	def is_community_can_add_list(self, community_id):
		return self.community.pk != community_id and community_id not in self.get_communities_ids()
	def is_community_can_delete_list(self, community_id):
		return self.community.pk != community_id and community_id in self.get_communities_ids()

	def get_cover(self):
		if self.image:
			return self.image.url
		else:
			return '/static/images/no_img/list.jpg'

	@classmethod
	def get_user_staff_lists(cls, user_pk):
		query = ~Q(type__contains="THIS")
		query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
		return cls.objects.filter(query)
	@classmethod
	def is_have_user_staff_lists(cls, user_pk):
		query = ~Q(type__contains="THIS")
		query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
		return cls.objects.filter(query).exists()
	@classmethod
	def get_user_lists(cls, user_pk):
		query = Q(type="LIS")
		query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
		return cls.objects.filter(query).order_by("order")
	@classmethod
	def is_have_user_lists(cls, user_pk):
		query = Q(type="LIS")
		query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
		return cls.objects.filter(query).exists()
	@classmethod
	def get_user_lists_count(cls, user_pk):
		query = Q(type="LIS")
		query.add(Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)), Q.AND)
		return cls.objects.filter(query).values("pk").count()

	@classmethod
	def get_community_staff_lists(cls, community_pk):
		query = ~Q(type__contains="THIS")
		query.add(Q(Q(community_id=user_pk)|Q(communities__id=user_pk)), Q.AND)
		return cls.objects.filter(query)
	@classmethod
	def is_have_community_staff_lists(cls, community_pk):
		query = ~Q(type__contains="THIS")
		query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
		return cls.objects.filter(query).exists()
	@classmethod
	def get_community_lists(cls, community_pk):
		query = Q(type="LIS")
		query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
		return cls.objects.filter(query).order_by("order")
	@classmethod
	def is_have_community_lists(cls, community_pk):
		query = Q(type="LIS")
		query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
		return cls.objects.filter(query).exists()
	@classmethod
	def get_community_lists_count(cls, community_pk):
		query = Q(type="LIS")
		query.add(Q(Q(community_id=community_pk)|Q(communities__id=user_pk)), Q.AND)
		return cls.objects.filter(query).values("pk").count()

	@classmethod
	def create_list(cls, creator, name, description, order, community, is_public):
		from notify.models import Notify, Wall
		from common.processing.good import get_good_list_processing
		if not order:
			order = 1
		if community:
			list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
			get_good_list_processing(list, GoodList.LIST)
			if is_public:
				from common.notify.progs import community_send_notify, community_send_wall
				Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="GOL", object_id=list.pk, verb="ITE")
				community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_good_list_wall")
				for user_id in community.get_member_for_notify_ids():
					Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="GOL", object_id=list.pk, verb="ITE")
					community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_good_list_notify")
		else:
			list = cls.objects.create(creator=creator,name=name,description=description, order=order)
			get_good_list_processing(list, GoodList.LIST)
			if is_public:
				from common.notify.progs import user_send_notify, user_send_wall
				Wall.objects.create(creator_id=creator.pk, type="GOL", object_id=list.pk, verb="ITE")
				user_send_wall(list.pk, None, "create_u_good_list_wall")
				for user_id in creator.get_user_news_notify_ids():
					Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="GOL", object_id=list.pk, verb="ITE")
					user_send_notify(list.pk, creator.pk, user_id, None, "create_u_good_list_notify")
		return list
	def edit_list(self, name, description, order, is_public):
		from common.processing.good import get_good_list_processing
		if not order:
			order = 1
		self.name = name
		self.description = description
		self.order = order
		self.save()
		if is_public:
			get_good_list_processing(self, GoodList.LIST)
			self.make_publish()
		else:
			get_good_list_processing(self, GoodList.PRIVATE)
			self.make_private()
		return self

	def make_private(self):
		from notify.models import Notify, Wall
		self.type = GoodList.PRIVATE
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def make_publish(self):
		from notify.models import Notify, Wall
		self.type = GoodList.LIST
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
	def delete_list(self):
		from notify.models import Notify, Wall
		if self.type == "LIS":
			self.type = GoodList.THIS_DELETED
		elif self.type == "PRI":
			self.type = GoodList.THIS_DELETED_PRIVATE
		elif self.type == "MAN":
			self.type = GoodList.THIS_DELETED_MANAGER
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def abort_delete_list(self):
		from notify.models import Notify, Wall
		if self.type == "TDEL":
			self.type = GoodList.LIST
		elif self.type == "TDELP":
			self.type = GoodList.PRIVATE
		elif self.type == "TDELM":
			self.type = GoodList.MANAGER
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")

	def close_list(self):
		from notify.models import Notify, Wall
		if self.type == "LIS":
			self.type = GoodList.THIS_CLOSED
		elif self.type == "MAI":
			self.type = GoodList.THIS_CLOSED_MAIN
		elif self.type == "PRI":
			self.type = GoodList.THIS_CLOSED_PRIVATE
		elif self.type == "MAN":
			self.type = GoodList.THIS_CLOSED_MANAGER
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def abort_close_list(self):
		from notify.models import Notify, Wall
		if self.type == "TCLO":
			self.type = GoodList.LIST
		elif self.type == "TCLOM":
			self.type = GoodList.MAIN
		elif self.type == "TCLOP":
			self.type = GoodList.PRIVATE
		elif self.type == "TCLOM":
			self.type = GoodList.MANAGER
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")


class Good(models.Model):
	THIS_PROCESSING, DRAFT, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = 'PRO', 'DRA','PUB','PRI','MAN','TDEL','TCLO'
	THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = 'TDELP','TDELM','TCLOP','TCLOM'
	STATUS = (
		(THIS_PROCESSING, 'Обработка'),(DRAFT, 'Черновик'),(PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
		(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
	)
	title = models.CharField(max_length=200, verbose_name="Название")
	sub_category = models.ForeignKey(GoodSubCategory, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Подкатегория")
	price = models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена товара")
	description = models.TextField(max_length=1000, verbose_name="Описание товара")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_creator", on_delete=models.CASCADE, verbose_name="Создатель")
	image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 80}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_good_directory)
	status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=6, verbose_name="Статус")

	comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
	votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
	list = models.ManyToManyField(GoodList, related_name="good_list", blank=True)

	comments = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
	views = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
	ad_views = models.PositiveIntegerField(default=0, verbose_name="Кол-во рекламных просмотров")
	likes = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
	dislikes = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
	reposts = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

	def __str__(self):
		return self.title

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name="Товар"
		verbose_name_plural="Товары"
		ordering = ["-created"]

	def likes(self):
		likes = GoodVotes.objects.filter(parent=self, vote__gt=0)
		return likes

	def is_draft(self):
		if self.status == Good.DRAFT:
			return True
		else:
			return False

	def likes_count(self):
		likes = GoodVotes.objects.filter(parent=self, vote__gt=0).values("pk").count()
		if likes > 0:
			return likes
		else:
			return ''

	def window_likes(self):
		likes = GoodVotes.objects.filter(parent=self, vote__gt=0)
		return likes[0:6]

	def dislikes(self):
		dislikes = GoodVotes.objects.filter(parent=self, vote__lt=0)
		return dislikes

	def dislikes_count(self):
		dislikes = GoodVotes.objects.filter(parent=self, vote__lt=0).values("pk").count()
		if dislikes > 0:
			return dislikes
		else:
			return ''

	def window_dislikes(self):
		dislikes = GoodVotes.objects.filter(parent=self, vote__lt=0)
		return dislikes[0:6]

	def get_reposts(self):
		parents = Good.objects.filter(parent=self)
		return parents

	def get_window_reposts(self):
		parents = Good.objects.filter(parent=self)
		return parents[0:6]

	def count_reposts(self):
		parents = self.get_reposts()
		count_reposts = parents.count()
		return count_reposts

	def get_comments(self):
		comments_query = Q(good_id=self.pk)
		comments_query.add(Q(parent__isnull=True), Q.AND)
		return GoodComment.objects.filter(comments_query)
	def count_comments(self):
		parent_comments = GoodComment.objects.filter(good_id=self.pk, is_deleted=False).values("pk")
		parents_count = parent_comments.count()
		i = 0
		for comment in parent_comments:
			i = i + comment.count_replies()
		i = i + parents_count
		return i

	def all_visits_count(self):
		from stst.models import GoodNumbers

		count = GoodNumbers.objects.filter(good=self.pk).values('pk').count()
		a = count % 10
		b = count % 100
		if (a == 1) and (b != 11):
			return str(count) + " просмотр"
		elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
			return str(count) + " просмотра"
		else:
			return str(count) + " просмотров"

	def visits_count(self):
		from stst.models import GoodNumbers
		return GoodNumbers.objects.filter(good=self.pk).values('pk').count()

	def get_lists_for_good(self):
		return self.list.all()

	def get_list_uuid(self):
		return self.list.all()[0].uuid

	def get_images(self):
		return GoodImage.objects.filter(good_id=self.pk)

	@classmethod
	def create_good(cls, creator, description, votes_on, comments_enabled, title, image, images, price, lists, sub_category, community, is_public):
		from common.processing.good import get_good_processing
		if not lists:
			from rest_framework.exceptions import ValidationError
			raise ValidationError("Не выбран список для нового Товара")
		private = 0
		if not price:
			price = 0
		good = cls.objects.create(creator=creator,title=title,description=description,votes_on=votes_on,comments_enabled=comments_enabled,image=image,price=price,sub_category=sub_category,community=community)
		for img in images:
			GoodImage.objects.create(good=good, image=img)
		for list_id in lists:
			good_list = GoodList.objects.get(pk=list_id)
			good_list.good_list.add(good)
			if good_list.is_private():
				private = 1
		if not private and is_public:
			get_good_processing(good, Good.PUBLISHED)
			if community:
				from common.notify.progs import community_send_notify, community_send_wall
				from notify.models import Notify, Wall

				Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="GOO", object_id=good.pk, verb="ITE")
				community_send_wall(good.pk, creator.pk, community.pk, None, "create_c_good_wall")
				for user_id in community.get_member_for_notify_ids():
					Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="GOO", object_id=good.pk, verb="ITE")
					community_send_notify(good.pk, creator.pk, user_id, community.pk, None, "create_c_good_notify")
			else:
				from common.notify.progs import user_send_notify, user_send_wall
				from notify.models import Notify, Wall

				Wall.objects.create(creator_id=creator.pk, type="GOO", object_id=good.pk, verb="ITE")
				user_send_wall(good.pk, None, "create_u_good_wall")
				for user_id in creator.get_user_news_notify_ids():
					Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="GOO", object_id=good.pk, verb="ITE")
					user_send_notify(good.pk, creator.pk, user_id, None, "create_u_good_notify")
		else:
			get_good_processing(good, Good.PRIVATE)
			return good

	def edit_good(self, description, votes_on, comments_enabled, title, image, images, price, lists, sub_category, community, is_public):
		from common.processing.good import get_good_processing
		self.title = title
		self.description = description
		self.lists = lists
		self.votes_on = votes_on
		self.comments_enabled = comments_enabled
		self.image = image
		self.price = price
		self.sub_category = sub_category
		self.community = community
		if is_public:
			get_good_processing(self, Good.PUBLISHED)
			self.make_publish()
		else:
			get_good_processing(self, Good.PRIVATE)
			self.make_private()
		if images:
			for image in images:
				GoodImage.objects.create(good=good, image=image)
		return self.save()

	def make_private(self):
		from notify.models import Notify, Wall
		self.status = Good.PRIVATE
		self.save(update_fields=['status'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def make_publish(self):
		from notify.models import Notify, Wall
		self.status = Good.PUBLISHED
		self.save(update_fields=['status'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")

	def delete_good(self):
		from notify.models import Notify, Wall
		if self.status == "PUB":
			self.status = Good.THIS_DELETED
		elif self.status == "PRI":
			self.status = Good.THIS_DELETED_PRIVATE
		elif self.status == "MAN":
			self.status = Good.THIS_DELETED_MANAGER
		self.save(update_fields=['status'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def abort_delete_good(self):
		from notify.models import Notify, Wall
		if self.status == "TDEL":
			self.status = Good.PUBLISHED
		elif self.status == "TDELP":
			self.status = Good.PRIVATE
		elif self.status == "TDELM":
			self.status = Good.MANAGER
		self.save(update_fields=['status'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")

	def close_good(self):
	    from notify.models import Notify, Wall
	    if self.status == "PUB":
	        self.status = Good.THIS_CLOSED
	    elif self.status == "PRI":
	        self.status = Good.THIS_CLOSED_PRIVATE
	    elif self.status == "MAN":
	        self.status = Good.THIS_CLOSED_MANAGER
	    self.save(update_fields=['status'])
	    if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
	        Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	    if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
	        Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def abort_close_good(self):
	    from notify.models import Notify, Wall
	    if self.status == "TCLO":
	        self.status = Good.PUBLISHED
	    elif self.status == "TCLOP":
	        self.status = Good.PRIVATE
	    elif self.status == "TCLOM":
	        self.status = Good.MANAGER
	    self.save(update_fields=['status'])
	    if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
	        Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
	    if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
	        Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")


class GoodImage(models.Model):
	good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
	image = ProcessedImageField(verbose_name='Изображение', format='JPEG',options={'quality': 100}, processors=[Transpose(), ResizeToFit(1000,1000)],upload_to=upload_to_good_directory)

	def __str__(self):
		return str(self.pk)


class GoodComment(models.Model):
	EDITED, PUBLISHED, THIS_PROCESSING = 'EDI', 'PUB', 'PRO'
	THIS_DELETED, THIS_EDITED_DELETED = 'TDEL', 'TDELE'
	THIS_CLOSED, THIS_EDITED_CLOSED = 'TCLO', 'TCLOE'
	STATUS = (
	(PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(THIS_PROCESSING, 'Обработка'),
		(THIS_DELETED, 'Удалённый'), (THIS_EDITED_DELETED, 'Удалённый изменённый'),
		(THIS_CLOSED, 'Закрытый менеджером'), (THIS_EDITED_CLOSED, 'Закрытый изменённый'),
	)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='good_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
	text = models.TextField(blank=True,null=True)
	comment = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
	attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
	status = models.CharField(max_length=5, choices=STATUS, default=THIS_PROCESSING, verbose_name="Тип альбома")

	likes = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
	dislikes = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
	reposts = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

	class Meta:
		indexes = (BrinIndex(fields=['created']), )
		verbose_name = "комментарий к записи"
		verbose_name_plural = "комментарии к записи"

	def __str__(self):
		return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

	def get_replies(self):
		get_comments = GoodComment.objects.filter(parent=self).all()
		return get_comments

	def count_replies(self):
		return self.good_comment_replies.filter(is_deleted=False).values("pk").count()

	def likes(self):
		likes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)
		return likes

	def window_likes(self):
		likes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)
		return likes[0:6]

	def dislikes(self):
		dislikes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)
		return dislikes

	def window_dislikes(self):
		dislikes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)
		return dislikes[0:6]

	def likes_count(self):
		likes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__gt=0).values("pk").count()
		if likes > 0:
			return likes
		else:
			return ''

	def dislikes_count(self):
		dislikes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__lt=0).values("pk").count()
		if dislikes > 0:
			return dislikes
		else:
			return ''

	@classmethod
	def create_comment(cls, commenter, attach, good, parent, text):
		from common.notify.notify import community_wall, community_notify, user_wall, user_notify
		from django.utils import timezone

		_attach = str(attach)
		_attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
		comment = GoodComment.objects.create(commenter=commenter, attach=_attach, parent=parent, good=good, text=text, created=timezone.now())
		if comment.parent:
			good = comment.parent.good
			type = "gor"+str(comment.pk)+",goc"+str(comment.parent.pk)+",goo"+str(post.pk)
			if good.community:
				community_wall(commenter, community, None, type, "c_good_comment_notify", "REP")
				community_notify(commenter, community, None, type, "c_good_comment_notify", "REP")
			else:
				user_wall(commenter, None, type, "u_good_comment_notify", "REP")
				user_notify(commenter, good.creator.pk, None, type, "u_good_comment_notify", "REP")
		else:
			type = "goc"+str(comment.pk)+", goo"+str(good.pk)
			if comment.good.community:
				community_wall(commenter, community, None, type, "c_good_comment_notify", "COM")
				community_notify(commenter, community, None, type, "c_good_comment_notify", "COM")
			else:
				user_wall(commenter, None, type, "u_good_comment_notify", "COM")
				user_notify(commenter, good.creator.pk, None, type, "u_good_comment_notify", "COM")
		return comment

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	def count_replies_ru(self):
		count = self.good_comment_replies.filter(is_deleted=False).values("pk").count()
		a = count % 10
		b = count % 100
		if (a == 1) and (b != 11):
			return str(count) + " ответ"
		elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
			return str(count) + " ответа"
		else:
			return str(count) + " ответов"

	def get_u_attach(self, user):
		from common.attach.comment_attach import get_u_comment_attach
		return get_u_comment_attach(self, user)

	def get_c_attach(self, user):
		from common.attach.comment_attach import get_c_comment_attach
		return get_c_comment_attach(self, user)

	def delete_comment(self):
		try:
			from notify.models import Notify
			if self.parent:
				Notify.objects.filter(attach="gor" + str(self.pk)).update(status="C")
			else:
				Notify.objects.filter(attach="goc" + str(self.pk)).update(status="C")
		except:
			pass
		self.is_deleted = True
		return self.save(update_fields=['is_deleted'])

	def abort_delete_comment(self):
		try:
			from notify.models import Notify
			if self.parent:
				Notify.objects.filter(attach="gor" + str(self.pk)).update(status="R")
			else:
				Notify.objects.filter(attach="goc" + str(self.pk)).update(status="R")
		except:
			pass
		self.is_deleted = False
		return self.save(update_fields=['is_deleted'])
