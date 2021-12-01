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
from communities.models import Community
from common.model.other import Stickers


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
	MAIN, LIST, MANAGER = 'MAI','LIS','MAN',
	DELETED, DELETED_MANAGER = '_DEL','_DELM'
	CLOSED, CLOSED_MAIN, CLOSED_MANAGER = '_CLO','_CLOM','_CLOMA'
	ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
	TYPE = (
		(MAIN, 'Основной'),(LIST, 'Пользовательский'),(MANAGER, 'Созданный персоналом'),
		(DELETED, 'Удалённый'),(DELETED_MANAGER, 'Удалённый менеджерский'),
		(CLOSED, 'Закрытый менеджером'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
		)

	PERM = (
		(ALL_CAN, 'Все пользователи'),
		(FRIENDS, 'Друзья'),
		(EACH_OTHER, 'Друзья,друзья друзей'),
		(CREATOR, 'Только я'),
		(FRIENDS_BUT, 'Друзья, кроме'),
		(SOME_FRIENDS, 'Некоторые друзья'),
		(MEMBERS, 'Подписчики'),
		(ADMINS, 'Администраторы'),
		(MEMBERS_BUT, 'Подписчики, кроме'),
		(SOME_MEMBERS, 'Некоторые подписчики'),
	)

	community = models.ForeignKey('communities.Community', related_name='good_lists_community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
	uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
	name = models.CharField(max_length=250, verbose_name="Название")
	type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип альбома")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_list_creator', verbose_name="Создатель")
	description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

	users = models.ManyToManyField("users.User", blank=True, related_name='+')
	communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')
	count = models.PositiveIntegerField(default=0)

	can_see_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит записи")
	can_see_comment = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит комментарии")
	create_el = models.PositiveSmallIntegerField(choices=PERM, default=7, verbose_name="Кто создает записи и потом с этими документами работает")
	create_comment = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет комментарии")
	copy_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто может копировать")
	is_good_list = models.BooleanField(default=True)

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name = 'Подборка товаров'
		verbose_name_plural = 'Подборки товаров'

	def __str__(self):
		return self.name

	def add_in_community_collections(self, community):
		from communities.model.list import CommunityGoodListPosition
		CommunityGoodListPosition.objects.create(community=community.pk, list=self.pk, position=GoodList.get_community_lists_count(community.pk))
		self.communities.add(community)
	def remove_in_community_collections(self, community):
		from communities.model.list import CommunityGoodListPosition
		CommunityGoodListPosition.objects.get(community=community.pk, list=self.pk).delete()
		self.communities.remove(user)
	def add_in_user_collections(self, user):
		from users.model.list import UserGoodListPosition
		UserGoodListPosition.objects.create(user=user.pk, list=self.pk, position=GoodList.get_user_lists_count(user.pk))
		self.users.add(user)
	def remove_in_user_collections(self, user):
		from users.model.list import UserGoodListPosition
		UserGoodListPosition.objects.get(user=user.pk, list=self.pk).delete()
		self.users.remove(user)

	@receiver(post_save, sender=Community)
	def create_c_model(sender, instance, created, **kwargs):
		if created:
			list = GoodList.objects.create(community=instance, type=GoodList.MAIN, name="Основной список", creator=instance.creator)
			from communities.model.list import CommunityGoodListPosition
			CommunityGoodListPosition.objects.create(community=instance.pk, list=list.pk, position=1)

	def is_main(self):
		return self.type == self.MAIN
	def is_list(self):
		return self.type == self.LIST
	def is_private(self):
		return False
	def is_open(self):
		return self.type[0] != "_"
	def is_have_edit(self):
		return self.is_list() or self.is_private()
	def is_deleted(self):
		return self.type[:4] == "_DEL"
	def is_closed(self):
		return self.type[:4] == "_CLO"

	def get_items(self):
		return self.good_list.filter(type="PUB")
	def get_staff_items(self):
		return self.good_list.filter(Q(type="PUB")|Q(type="PRI"))
	def count_items(self):
		try:
			return self.good_list.filter(type="PUB").values("pk").count()
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
		 return self.good_list.filter(type="PUB").values("pk").exists()
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

	def get_cover(self):
		if self.image:
			return self.image.url
		else:
			return '/static/images/no_img/list.jpg'

	@classmethod
	def get_user_staff_lists(cls, user_pk):
		try:
			from users.model.list import UserGoodListPosition
			query = []
			lists = UserGoodListPosition.objects.filter(user=user_pk, type=1).values("list")
			for list_id in [i['list'] for i in lists]:
				list = cls.objects.get(pk=list_id)
				if list.type[0] != "_":
					query.append(list)
			return query
		except:
			query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
			query.add(~Q(type__contains="_"), Q.AND)
			return cls.objects.filter(query)
	@classmethod
	def get_user_lists(cls, user_pk):
		try:
			from users.model.list import UserGoodListPosition
			query = []
			lists = UserGoodListPosition.objects.filter(user=user_pk, type=1).values("list")
			for list_id in [i['list'] for i in lists]:
				list = cls.objects.get(pk=list_id)
				if list.is_have_get():
					query.append(list)
			return query
		except:
			query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
			query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
			return cls.objects.filter(query)
	@classmethod
	def get_user_lists_count(cls, user_pk):
		query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
		query.add(~Q(type__contains="_"), Q.AND)
		return cls.objects.filter(query).values("pk").count()

	@classmethod
	def get_community_staff_lists(cls, community_pk):
		try:
			from communities.model.list import CommunityGoodListPosition
			query = []
			lists = CommunityGoodListPosition.objects.filter(community=community_pk, type=1).values("list")
			for list_id in [i['list'] for i in lists]:
				list = cls.objects.get(pk=list_id)
				if list.type[0] != "_":
					query.append(list)
			return query
		except:
			query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
			query.add(~Q(type__contains="_"), Q.AND)
			return cls.objects.filter(query)
	@classmethod
	def get_community_lists(cls, community_pk):
		try:
			from communities.model.list import CommunityGoodListPosition
			query = []
			lists = CommunityGoodListPosition.objects.filter(community=community_pk, type=1).values("list")
			for list_id in [i['list'] for i in lists]:
				list = cls.objects.get(pk=list_id)
				if list.is_have_get():
					query.append(list)
				return query
		except:
			query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
			query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
			return cls.objects.filter(query)
	@classmethod
	def get_community_lists_count(cls, community_pk):
		query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
		query.add(~Q(type__contains="_"), Q.AND)
		return cls.objects.filter(query).values("pk").count()

	@classmethod
	def create_list(cls, creator, name, description, community):
		from notify.models import Notify, Wall
		from common.processing.good import get_good_list_processing

		list = cls.objects.create(creator=creator,name=name,description=description, community=community)
		is_public = True
		if community:
			from communities.model.list import CommunityGoodListPosition
			CommunityGoodListPosition.objects.create(community=community.pk, list=list.pk, position=GoodList.get_community_lists_count(community.pk))
			get_good_list_processing(list, GoodList.LIST)
			if is_public:
				from common.notify.progs import community_send_notify, community_send_wall
				Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="GOL", object_id=list.pk, verb="ITE")
				community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_good_list_wall")
				for user_id in community.get_member_for_notify_ids():
					Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="GOL", object_id=list.pk, verb="ITE")
					community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_good_list_notify")
		else:
			from users.model.list import UserGoodListPosition
			UserGoodListPosition.objects.create(user=creator.pk, list=list.pk, position=GoodList.get_user_lists_count(creator.pk))
			get_good_list_processing(list, GoodList.LIST)
			if is_public:
				from common.notify.progs import user_send_notify, user_send_wall
				Wall.objects.create(creator_id=creator.pk, type="GOL", object_id=list.pk, verb="ITE")
				user_send_wall(list.pk, None, "create_u_good_list_wall")
				for user_id in creator.get_user_news_notify_ids():
					Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="GOL", object_id=list.pk, verb="ITE")
					user_send_notify(list.pk, creator.pk, user_id, None, "create_u_good_list_notify")
		return list
	def edit_list(self, name, description):
		from common.processing.good import get_good_list_processing

		self.name = name
		self.description = description
		self.save()
		is_public = True
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
		if Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="C")
	def make_publish(self):
		from notify.models import Notify, Wall
		self.type = GoodList.LIST
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="R")
	def delete_item(self):
		from notify.models import Notify, Wall
		if self.type == "LIS":
			self.type = GoodList.DELETED
		elif self.type == "MAN":
			self.type = GoodList.DELETED_MANAGER
		self.save(update_fields=['type'])
		if self.community:
			from communities.model.list import CommunityGoodListPosition
			CommunityGoodListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
		else:
			from users.model.list import UserGoodListPosition
			UserGoodListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
		if Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="C")
	def restore_item(self):
		from notify.models import Notify, Wall
		if self.type == "_DEL":
			self.type = GoodList.LIST
		elif self.type == "_DELM":
			self.type = GoodList.MANAGER
		self.save(update_fields=['type'])
		if self.community:
			from communities.model.list import CommunityGoodListPosition
			CommunityGoodListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
		else:
			from users.model.list import UserGoodListPosition
			UserGoodListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
		if Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="R")

	def close_item(self):
		from notify.models import Notify, Wall
		if self.type == "LIS":
			self.type = GoodList.CLOSED
		elif self.type == "MAI":
			self.type = GoodList.CLOSED_MAIN
		elif self.type == "MAN":
			self.type = GoodList.CLOSED_MANAGER
		self.save(update_fields=['type'])
		if self.community:
			from communities.model.list import CommunityGoodListPosition
			CommunityGoodListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
		else:
			from users.model.list import UserGoodListPosition
			UserGoodListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
		if Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="C")
	def abort_close_item(self):
		from notify.models import Notify, Wall
		if self.type == "_CLO":
			self.type = GoodList.LIST
		elif self.type == "_CLOM":
			self.type = GoodList.MAIN
		elif self.type == "_CLOM":
			self.type = GoodList.MANAGER
		self.save(update_fields=['type'])
		if self.community:
			from communities.model.list import CommunityGoodListPosition
			CommunityGoodListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
		else:
			from users.model.list import UserGoodListPosition
			UserGoodListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
		if Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOL", object_id=self.pk, verb="ITE").update(status="R")


class Good(models.Model):
	DRAFT, PUBLISHED, MANAGER, DELETED, CLOSED = '_DRA','PUB','MAN','_DEL','_CLO'
	DELETED_MANAGER, CLOSED_MANAGER = '_DELM','_CLOM'
	TYPE = (
		(DRAFT, 'Черновик'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
		(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
	)
	title = models.CharField(max_length=200, verbose_name="Название")
	sub_category = models.ForeignKey(GoodSubCategory, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Подкатегория")
	price = models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена товара")
	description = models.TextField(max_length=1000, verbose_name="Описание товара")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_creator", on_delete=models.CASCADE, verbose_name="Создатель")
	image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 80}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_good_directory)
	type = models.CharField(choices=TYPE, max_length=6, verbose_name="Статус")

	comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
	votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
	list = models.ForeignKey(GoodList, on_delete=models.SET_NULL, related_name='good_list', blank=True, null=True)
	community = models.ForeignKey('communities.Community', related_name='good_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

	comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
	view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
	ad_view = models.PositiveIntegerField(default=0, verbose_name="Кол-во рекламных просмотров")
	like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
	dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
	repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
	order = models.PositiveIntegerField(default=0)
	is_good = models.BooleanField(default=True)

	def __str__(self):
		return self.title

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name="Товар"
		verbose_name_plural="Товары"
		ordering = ["-order"]

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	def plus_comments(self, count):
		self.comment += count
		return self.save(update_fields=['comment'])
	def minus_comments(self, count):
		self.comment -= count
		return self.save(update_fields=['comment'])
	def plus_views(self, count):
		self.view += count
		return self.save(update_fields=['view'])
	def minus_views(self, count):
		self.view -= count
		return self.save(update_fields=['view'])
	def plus_reposts(self, count):
		self.repost += count
		return self.save(update_fields=['repost'])
	def minus_reposts(self, count):
		self.repost -= count
		return self.save(update_fields=['repost'])

	def likes(self):
		from common.model.votes import PhotoVotes
		return GoodVotes.objects.filter(parent=self, vote__gt=0)

	def is_draft(self):
		if self.type == Good.DRAFT:
			return True
		else:
			return False

	def likes_count(self):
		if self.like > 0:
			return self.like
		else:
			return ''

	def window_likes(self):
		from common.model.votes import GoodVotes
		return GoodVotes.objects.filter(parent=self, vote__gt=0)[0:6]

	def dislikes(self):
		from common.model.votes import GoodVotes
		return GoodVotes.objects.filter(parent=self, vote__lt=0)

	def dislikes_count(self):
		if self.dislike > 0:
			return self.dislike
		else:
			return ''

	def window_dislikes(self):
		from common.model.votes import GoodVotes
		return GoodVotes.objects.filter(parent=self, vote__lt=0)[0:6]

	def get_reposts(self):
		return Good.objects.filter(parent=self)

	def get_window_reposts(self):
		return Good.objects.filter(parent=self)[0:6]

	def count_reposts(self):
		if self.repost > 0:
			return self.repost
		else:
			return ''

	def get_comments(self):
		comments_query = Q(good_id=self.pk)
		comments_query.add(Q(parent__isnull=True), Q.AND)
		return GoodComment.objects.filter(comments_query)
	def count_comments(self):
		if self.comment > 0:
			return self.comment
		else:
			return ''

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

	def get_lists(self):
		return self.list.all()

	def get_list_uuid(self):
		return self.list.all()[0].uuid

	def get_images(self):
		return GoodImage.objects.filter(good_id=self.pk)

	@classmethod
	def create_good(cls, creator, description, votes_on, comments_enabled, title, image, images, price, list, sub_category, community):
		from common.processing.good import get_good_processing
		if not price:
			price = 0
		list.count += 1
		list.save(update_fields=["count"])
		good = cls.objects.create(creator=creator,order=list.count,title=title,list=list,description=description,votes_on=votes_on,comments_enabled=comments_enabled,image=image,price=price,sub_category=sub_category,community=community)
		for img in images:
			GoodImage.objects.create(good=good, image=img)
		get_good_processing(good, Good.PUBLISHED)
		if not list.is_private():
			if community:
				from common.notify.progs import community_send_notify, community_send_wall
				from notify.models import Notify, Wall

				Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="GOO", object_id=good.pk, verb="ITE")
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
		if community:
			community.plus_goods(1)
		else:
			creator.plus_goods(1)
		return good

	def edit_good(self, description, votes_on, comments_enabled, title, image, images, price, list, sub_category):
		from common.processing.good import get_good_processing
		self.title = title
		self.description = description
		if self.list.pk != list.pk:
			self.list.count -= 1
			self.list.save(update_fields=["count"])
			list.count += 1
			list.save(update_fields=["count"])
		self.votes_on = votes_on
		self.comments_enabled = comments_enabled
		self.image = image
		self.price = price
		self.list = list
		self.sub_category = sub_category
		self.community = community
		if images:
			for image in images:
				GoodImage.objects.create(good=good, image=image)
		return self.save()

	def make_private(self):
		from notify.models import Notify, Wall
		self.type = Good.PRIVATE
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def make_publish(self):
		from notify.models import Notify, Wall
		self.type = Good.PUBLISHED
		self.save(update_fields=['type'])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")

	def delete_item(self, community):
		from notify.models import Notify, Wall
		if self.type == "PUB":
			self.type = Good.DELETED
		elif self.type == "MAN":
			self.type = Good.DELETED_MANAGER
		self.save(update_fields=['type'])
		if community:
			community.minus_goods(1)
		else:
			self.creator.minus_goods(1)
		self.list.count -= 1
		self.list.save(update_fields=["count"])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def restore_item(self, community):
		from notify.models import Notify, Wall
		if self.type == "_DEL":
			self.type = Good.PUBLISHED
		elif self.type == "_DELM":
			self.type = Good.MANAGER
		self.save(update_fields=['type'])
		if community:
			community.plus_goods(1)
		else:
			self.creator.plus_goods(1)
		self.list.count += 1
		self.list.save(update_fields=["count"])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")

	def close_item(self, community):
		from notify.models import Notify, Wall
		if self.type == "PUB":
			self.type = Good.CLOSED
		elif self.type == "MAN":
			self.type = Good.CLOSED_MANAGER
		self.save(update_fields=['type'])
		if community:
			community.minus_goods(1)
		else:
			self.creator.minus_goods(1)
		self.list.count -= 1
		self.list.save(update_fields=["count"])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="C")
	def abort_close_item(self, community):
		from notify.models import Notify, Wall
		if self.type == "_CLO":
			self.type = Good.PUBLISHED
		elif self.type == "_CLOM":
			self.type = Good.MANAGER
		self.save(update_fields=['type'])
		if community:
			community.plus_goods(1)
		else:
			self.creator.plus_goods(1)
		self.list.count += 1
		self.list.save(update_fields=["count"])
		if Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Notify.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")
		if Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").exists():
			Wall.objects.filter(type="GOO", object_id=self.pk, verb="ITE").update(status="R")

	def send_like(self, user, community):
		import json
		from common.model.votes import GoodVotes
		from django.http import HttpResponse
		from common.notify.notify import user_notify, user_wall
		if not self.votes_on:
			from django.http import Http404
			raise Http404
		try:
			item = GoodVotes.objects.get(parent=self, user=user)
			if item.vote != GoodVotes.LIKE:
				item.vote = GoodVotes.LIKE
				item.save(update_fields=['vote'])
				self.like += 1
				self.dislike -= 1
				self.save(update_fields=['like', 'dislike'])
			else:
				item.delete()
				self.like -= 1
				self.save(update_fields=['like'])
		except GoodVotes.DoesNotExist:
			GoodVotes.objects.create(parent=self, user=user, vote=GoodVotes.LIKE)
			self.like += 1
			self.save(update_fields=['like'])
			if community:
				from common.notify.notify import community_notify, community_wall
				community_notify(user, community, None, self.pk, "GOO", "u_good_notify", "LIK")
				community_wall(user, community, None, self.pk, "GOO", "u_good_notify", "LIK")
			else:
				from common.notify.notify import user_notify, user_wall
				user_notify(user, None, self.pk, "GOO", "u_good_notify", "LIK")
				user_wall(user, None, self.pk, "GOO", "u_good_notify", "LIK")
		return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
	def send_dislike(self, user, community):
		import json
		from common.model.votes import GoodVotes
		from django.http import HttpResponse
		from common.notify.notify import user_notify, user_wall
		if not self.votes_on:
			from django.http import Http404
			raise Http404
		try:
			item = GoodVotes.objects.get(parent=self, user=user)
			if item.vote != GoodVotes.DISLIKE:
				item.vote = GoodVotes.DISLIKE
				item.save(update_fields=['vote'])
				self.like -= 1
				self.dislike += 1
				self.save(update_fields=['like', 'dislike'])
			else:
				item.delete()
				self.dislike -= 1
				self.save(update_fields=['dislike'])
		except GoodVotes.DoesNotExist:
			GoodVotes.objects.create(parent=self, user=user, vote=GoodVotes.DISLIKE)
			self.dislike += 1
			self.save(update_fields=['dislike'])
			if community:
				from common.notify.notify import community_notify, community_wall
				community_notify(user, community, None, self.pk, "GOO", "u_good_notify", "DIS")
				community_wall(user, community, None, self.pk, "GOO", "u_good_notify", "DIS")
			else:
				from common.notify.notify import user_notify, user_wall
				user_notify(user, None, self.pk, "GOO", "u_good_notify", "DIS")
				user_wall(user, None, self.pk, "GOO", "u_good_notify", "DIS")
		return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

	def is_deleted(self):
		return self.type[:4] == "_DEL"
	def is_closed(self):
		return self.type[:4] == "_CLO"


class GoodImage(models.Model):
	good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
	image = ProcessedImageField(verbose_name='Изображение', format='JPEG',options={'quality': 100}, processors=[Transpose(), ResizeToFit(1000,1000)],upload_to=upload_to_good_directory)

	def __str__(self):
		return str(self.pk)


class GoodComment(models.Model):
	EDITED, PUBLISHED, DRAFT = 'EDI','PUB','_DRA'
	DELETED, EDITED_DELETED = '_DEL', '_DELE'
	CLOSED, EDITED_CLOSED = '_CLO', '_CLOE'
	TYPE = (
		(PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(DRAFT, 'Черновик'),
		(DELETED, 'Удалённый'), (EDITED_DELETED, 'Удалённый изменённый'),
		(CLOSED, 'Закрытый менеджером'), (EDITED_CLOSED, 'Закрытый изменённый'),
	)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='good_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
	text = models.TextField(blank=True,null=True)
	good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
	attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
	type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип альбома")
	sticker = models.ForeignKey(Stickers, blank=True, null=True, on_delete=models.CASCADE, related_name="+")

	like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
	dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
	repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

	class Meta:
		indexes = (BrinIndex(fields=['created']), )
		verbose_name = "комментарий к записи"
		verbose_name_plural = "комментарии к записи"

	def __str__(self):
		return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

	def get_replies(self):
		return self.good_comment_replies.filter(Q(type=GoodComment.EDITED)|Q(type=GoodComment.PUBLISHED)).all()

	def count_replies(self):
		return self.get_replies().values("pk").count()

	def likes(self):
		from common.model.votes import GoodCommentVotes
		return GoodCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)

	def window_likes(self):
		from common.model.votes import GoodCommentVotes
		return GoodCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)[0:6]

	def dislikes(self):
		from common.model.votes import GoodCommentVotes
		return GoodCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)

	def window_dislikes(self):
		from common.model.votes import GoodCommentVotes
		return GoodCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)[0:6]

	def likes_count(self):
		if self.like > 0:
			return self.like
		else:
			return ''

	def dislikes_count(self):
		if self.dislike > 0:
			return self.dislike
		else:
			return ''

	def reposts_count(self):
		if self.repost > 0:
			return self.repost
		else:
			return ''

	@classmethod
	def create_comment(cls, commenter, attach, good, parent, text, community, sticker):
		from common.notify.notify import community_wall, community_notify, user_wall, user_notify
		from common.processing_2 import get_text_processing

		_attach = str(attach)
		_attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
		if sticker:
			comment = GoodComment.objects.create(commenter=commenter, sticker_id=sticker, parent=parent, good=good)
		else:
			comment = GoodComment.objects.create(commenter=commenter, attach=_attach, parent=parent, good=good, text=get_text_processing(text))
		good.comment += 1
		good.save(update_fields=["comment"])
		if comment.parent:
			if community:
				community_notify(comment.commenter, community, None, comment.pk, "GOOC", "u_good_comment_notify", "REP")
				community_wall(comment.commenter, community, None, comment.pk, "GOOC", "u_good_comment_notify", "REP")
			else:
				user_notify(comment.commenter, None, comment.pk, "GOOC", "u_good_comment_notify", "REP")
				user_wall(comment.commenter, None, comment.pk, "GOOC", "u_good_comment_notify", "REP")
		else:
			if comment.good.community:
				community_notify(comment.commenter, community, None, comment.pk, "GOOC", "u_good_comment_notify", "COM")
				community_wall(comment.commenter, community, None, comment.pk, "GOOC", "u_good_comment_notify", "COM")
			else:
				user_notify(comment.commenter, None, comment.pk, "GOOC", "u_good_comment_notify", "COM")
				user_wall(comment.commenter, None, comment.pk, "GOOC", "u_good_comment_notify", "COM")
		return comment

	def edit_comment(self, attach, text):
		from common.processing_2 import get_text_processing
		if not text and not attach:
			from rest_framework.exceptions import ValidationError
			raise ValidationError("Нет текста или прикрепленных элементов")

		_attach = str(attach)
		_attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
		self.attach = _attach
		self.text = get_text_processing(text)
		self.type = GoodComment.EDITED
		self.save()
		return self

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	def count_replies_ru(self):
		count = self.count_replies()
		a = count % 10
		b = count % 100
		if (a == 1) and (b != 11):
			return str(count) + " ответ"
		elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
			return str(count) + " ответа"
		else:
			return str(count) + " ответов"

	def get_attach(self, user):
		from common.attach.comment_attach import get_comment_attach
		return get_comment_attach(self, user)

	def send_like(self, user, community):
		import json
		from common.model.votes import GoodCommentVotes
		from django.http import HttpResponse
		from common.notify.notify import user_notify, user_wall
		try:
			item = GoodCommentVotes.objects.get(item=self, user=user)
			if item.vote != GoodCommentVotes.LIKE:
				item.vote = GoodCommentVotes.LIKE
				item.save(update_fields=['vote'])
				self.like += 1
				self.dislike -= 1
				self.save(update_fields=['like', 'dislike'])
			else:
				item.delete()
				self.like -= 1
				self.save(update_fields=['like'])
		except GoodCommentVotes.DoesNotExist:
			GoodCommentVotes.objects.create(item=self, user=user, vote=GoodCommentVotes.LIKE)
			self.like += 1
			self.save(update_fields=['like'])
			if self.parent:
				if community:
					from common.notify.notify import community_notify, community_wall
					community_notify(user, community, None, self.pk, "GOOC", "u_good_comment_notify", "LRE")
					community_wall(user, community, None, self.pk, "GOOC", "u_good_comment_notify", "LCO")
				else:
					from common.notify.notify import user_notify, user_wall
					user_notify(user, None, self.pk, "GOOC", "u_good_notify", "LRE")
					user_wall(user, None, self.pk, "GOOC", "u_good_notify", "LCO")
			else:
				if community:
					from common.notify.notify import community_notify, community_wall
					community_notify(user, community, None, self.pk, "GOOC", "u_good_comment_notify", "LCO")
					community_wall(user, community, None, self.pk, "GOOC", "u_good_comment_notify", "LCO")
				else:
					from common.notify.notify import user_notify, user_wall
					user_notify(user, None, self.pk, "GOOC", "u_good_comment_notify", "LCO")
					user_wall(user, None, self.pk, "GOOC", "u_good_comment_notify", "LCO")
		return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
	def send_dislike(self, user, community):
		import json
		from common.model.votes import GoodCommentVotes
		from django.http import HttpResponse
		from common.notify.notify import user_notify, user_wall
		try:
			item = GoodCommentVotes.objects.get(item=self, user=user)
			if item.vote != GoodCommentVotes.DISLIKE:
				item.vote = GoodCommentVotes.DISLIKE
				item.save(update_fields=['vote'])
				self.like -= 1
				self.dislike += 1
				self.save(update_fields=['like', 'dislike'])
			else:
				item.delete()
				self.dislike -= 1
				self.save(update_fields=['dislike'])
		except GoodCommentVotes.DoesNotExist:
			GoodCommentVotes.objects.create(item=self, user=user, vote=GoodCommentVotes.DISLIKE)
			self.dislike += 1
			self.save(update_fields=['dislike'])
			if self.parent:
				if community:
					from common.notify.notify import community_notify, community_wall
					community_notify(user, community, None, self.pk, "POSC", "u_good_comment_notify", "DRE")
					community_wall(user, community, None, self.pk, "POSC", "u_good_comment_notify", "DCO")
				else:
					from common.notify.notify import user_notify, user_wall
					user_notify(user, None, self.pk, "GOOC", "u_good_comment_notify", "DRE")
					user_wall(user, None, self.pk, "GOOC", "u_good_comment_notify", "DCO")
			else:
				if community:
					from common.notify.notify import community_notify, community_wall
					community_notify(user, community, None, self.pk, "POSC", "u_good_comment_notify", "DCO")
					community_wall(user, community, None, self.pk, "POSC", "u_good_comment_notify", "DCO")
				else:
					from common.notify.notify import user_notify, user_wall
					user_notify(user, None, self.pk, "GOOC", "u_good_comment_notify", "DCO")
					user_wall(user, None, self.pk, "GOOC", "u_good_comment_notify", "DCO")
		return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

	def delete_item(self):
		from notify.models import Notify, Wall
		if self.type == "PUB":
			self.type = GoodComment.DELETED
		elif self.type == "EDI":
			self.type = GoodComment.EDITED_DELETED
		self.save(update_fields=['type'])
		if self.parent:
			self.parent.good.comment -= 1
			self.parent.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").update(status="C")
		else:
			self.good.comment -= 1
			self.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").update(status="C")
		if Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").exists():
			Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").update(status="C")
	def restore_item(self):
		from notify.models import Notify, Wall
		if self.type == "_DEL":
			self.type = GoodComment.PUBLISHED
		elif self.type == "_DELE":
			self.type = GoodComment.EDITED
		self.save(update_fields=['type'])
		if self.parent:
			self.parent.good.comment += 1
			self.parent.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").update(status="R")
		else:
			self.good.comment += 1
			self.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").update(status="R")
		if Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").exists():
			Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").update(status="R")

	def close_item(self):
		from notify.models import Notify, Wall
		if self.type == "PUB":
			self.type = GoodComment.CLOSED
		elif self.type == "EDI":
			self.type = GoodComment.EDITED_CLOSED
		self.save(update_fields=['type'])
		if self.parent:
			self.parent.good.comment -= 1
			self.parent.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").update(status="C")
		else:
			self.good.comment -= 1
			self.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").update(status="C")
		if Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").exists():
			Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").update(status="C")
	def abort_close_item(self):
		from notify.models import Notify, Wall
		if self.type == "_CLO":
			self.type = GoodComment.PUBLISHED
		elif self.type == "_CLOE":
			self.type = GoodComment.EDITED
		self.save(update_fields=['type'])
		if self.parent:
			self.parent.good.comment += 1
			self.parent.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="REP").update(status="R")
		else:
			self.good.comment += 1
			self.good.save(update_fields=["comment"])
			if Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").exists():
				Notify.objects.filter(type="GOOC", object_id=self.pk, verb__contains="COM").update(status="R")
		if Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").exists():
			Wall.objects.filter(type="GOOC", object_id=self.pk, verb="COM").update(status="R")

	def is_private(self):
		return self.type == self.PRIVATE

	def get_edit_attach(self, user):
		from common.attach.comment_attach import get_comment_edit
		return get_comment_edit(self, user)

	def get_item(self):
		if self.parent:
			return self.parent.good
		else:
			return self.good

	def get_format_text(self):
		from common.utils import hide_text
		return hide_text(self.text)
