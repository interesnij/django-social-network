from django.db import models
import uuid
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from common.model.votes import GoodVotes, GoodCommentVotes
from django.db.models import Q
from goods.helpers import upload_to_good_directory, upload_to_sub_good_directory


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
	image = models.ImageField(blank=True, verbose_name="Изображение", upload_to="sub_category/list")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["order","name"]
		verbose_name = "Подкатегория товаров"
		verbose_name_plural = "Подкатегории товаров"


class GoodAlbum(models.Model):
    MAIN = 'MA'
    ALBUM = 'AL'
    TYPE = (
        (MAIN, 'Основной альбом'),
        (ALBUM, 'Пользовательский альбом'),
    )

    community = models.ForeignKey('communities.Community', related_name='good_album_community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    type = models.CharField(max_length=5, choices=TYPE, default=MAIN, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_album_creator', verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False)
    image = ProcessedImageField(verbose_name='Обложка', blank=True, format='JPEG',options={'quality': 100}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_good_directory)

    users = models.ManyToManyField("users.User", blank=True, related_name='users_good_album')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='communities_good_album')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Подборка товаров'
        verbose_name_plural = 'Подборки товаров'

    def is_main_album(self):
        return self.type == self.MAIN
    def is_user_album(self):
        return self.type == self.ALBUM

    def __str__(self):
        return self.title

    def get_2_goods(self):
        return self.good_album.filter(is_deleted=False)[:2]
    def get_3_goods(self):
        return self.good_album.filter(is_deleted=False)[:3]

    def count_goods(self):
        try:
            return self.good_album.filter(is_deleted=False).values("pk").count()
        except:
            return 0

    def count_goods_ru(self):
	    count = self.count_goods()
	    a, b = count % 10, count % 100
	    if (a == 1) and (b != 11):
		    return str(count) + " товар"
	    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
		    return str(count) + " товара"
	    else:
		    return str(count) + " товаров"

    def get_goods(self):
        return self.good_album.filter(is_deleted=False, status=Good.STATUS_PUBLISHED)

    def get_staff_goods(self):
        return self.good_album.filter(is_deleted=False)

    def is_not_empty(self):
	    return self.good_album.filter(album=self).values("pk").exists()

    def get_users_ids(self):
        users = self.users.exclude(perm="DE").exclude(perm="BL").exclude(perm="PV").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(perm="DE").exclude(perm="BL").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        if self.creator.pk != user_id and user_id not in self.get_users_ids():
            return True
        else:
            return False
    def is_user_can_delete_list(self, user_id):
        if self.creator.pk != user_id and user_id in self.get_users_ids():
            return True
        else:
            return False
    def is_community_can_add_list(self, community_id):
        if self.community.pk != community_id and community_id not in self.get_communities_ids():
            return True
        else:
            return False
    def is_community_can_delete_list(self, community_id):
        if self.community.pk != community_id and community_id in self.get_communities_ids():
            return True
        else:
            return False
    def get_cover(self):
	    if self.image:
		    return self.image.url
	    else:
		    return '/static/images/no_img/album.jpg'



class Good(models.Model):
	STATUS_DRAFT = 'D'
	STATUS_SOLD = 'S'
	STATUS_PUBLISHED = 'P'
	STATUS_PROCESSING = 'PG'
	STATUSES = (
		(STATUS_DRAFT, 'Отложен'),
		(STATUS_PUBLISHED, 'Опубликован'),
		(STATUS_SOLD, 'Продан'),
		(STATUS_PROCESSING, 'Обработка'),
		)
	id = models.BigAutoField(primary_key=True)
	title = models.CharField(max_length=200, verbose_name="Название")
	sub_category = models.ForeignKey(GoodSubCategory, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Подкатегория")
	price = models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена товара")
	description = models.TextField(max_length=1000, verbose_name="Описание товара")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_creator", on_delete=models.CASCADE, verbose_name="Создатель")
	image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 80}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_good_directory)
	status = models.CharField(choices=STATUSES, default=STATUS_PROCESSING, max_length=2, verbose_name="Статус")

	comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
	votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
	is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
	album = models.ManyToManyField(GoodAlbum, related_name="good_album", blank=True)

	def __str__(self):
		return self.title

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	@classmethod
	def create_good(cls, title, image, albums, images, sub_category, creator, description, \
					price, comments_enabled, votes_on, status):
		good = Good.objects.create(title=title, image=image, sub_category=sub_category, creator=creator, description=description, \
								status=status, price=price, comments_enabled=comments_enabled, votes_on=votes_on,)
		channel_layer = get_channel_layer()
		payload = {
			"type": "receive",
			"key": "additional_post",
			"actor_name": good.creator.get_full_name()
			}
		async_to_sync(channel_layer.group_send)('notifications', payload)
		if images:
			for image in images:
				GoodImage.objects.create(good=good, image=image)
		if albums:
			for album in albums:
				album.good_album.add(good)
		return good

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name="Товар"
		verbose_name_plural="Товары"
		ordering = ["-created"]

	def likes(self):
		likes = GoodVotes.objects.filter(parent=self, vote__gt=0)
		return likes

	def is_draft(self):
		if self.status == Good.STATUS_DRAFT:
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

	def get_albums_for_good(self):
		return self.album.all()

	def get_album_uuid(self):
		return self.album.all()[0].uuid

	def get_images(self):
		return GoodImage.objects.filter(good_id=self.pk)

	def delete_good(self):
		try:
			from notify.models import Notify
			Notify.objects.filter(attach="goo" + str(self.pk)).update(status="C")
		except:
			pass
		self.is_deleted = True
		return self.save(update_fields=['is_deleted'])

	def abort_delete_good(self):
		try:
			from notify.models import Notify
			Notify.objects.filter(attach="goo" + str(self.pk)).update(status="R")
		except:
			pass
		self.is_deleted = False
		return self.save(update_fields=['is_deleted'])


class GoodImage(models.Model):
	good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
	image = ProcessedImageField(verbose_name='Изображение', format='JPEG',options={'quality': 100}, processors=[Transpose(), ResizeToFit(1000,1000)],upload_to=upload_to_sub_good_directory)

	def __str__(self):
		return str(self.pk)


class GoodComment(models.Model):
	id = models.BigAutoField(primary_key=True)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='good_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
	text = models.TextField(blank=True,null=True)
	is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
	is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
	comment = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
	attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")

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
