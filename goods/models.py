from django.db import models
import uuid
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notify.model.good import *
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from common.model.votes import GoodVotes, GoodCommentVotes
from django.db.models import Q
from goods.helpers import upload_to_good_directory


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
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    type = models.CharField(max_length=5, choices=TYPE, default=MAIN, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_album_creator', verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )

    post = models.ManyToManyField("posts.Post", blank=True, related_name='post_good_album')
    message = models.ManyToManyField('chat.Message', blank=True, related_name='message_good_album')

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

    def get_goods(self):
        return self.good_album.filter(is_deleted=False, status=Good.STATUS_PUBLISHED)

    def get_staff_goods(self):
        return self.good_album.filter(is_deleted=False)

    def is_not_empty(self):
	    return self.good_album.filter(album=self).values("pk").exists()


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

	title = models.CharField(max_length=200, verbose_name="Название")
	sub_category = models.ForeignKey(GoodSubCategory, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Подкатегория")
	price = models.PositiveIntegerField(default=0, verbose_name="Цена товара")
	description = models.TextField(max_length=1000, verbose_name="Описание товара")
	comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
	votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_creator", on_delete=models.CASCADE, verbose_name="Создатель")
	is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
	id = models.BigAutoField(primary_key=True)
	album = models.ManyToManyField(GoodAlbum, related_name="good_album", blank=True, verbose_name="Подборка")

	image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512,512)],upload_to=upload_to_good_directory)
	image2 = ProcessedImageField(verbose_name='изображение 2', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFill(512, 512)],upload_to=upload_to_good_directory)
	image3 = ProcessedImageField(verbose_name='изображение 3', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to=upload_to_good_directory)
	image4 = ProcessedImageField(verbose_name='изображение 4', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to=upload_to_good_directory)
	image5 = ProcessedImageField(verbose_name='изображение 5', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to=upload_to_good_directory)
	status = models.CharField(choices=STATUSES, default=STATUS_PROCESSING, max_length=2, verbose_name="Статус")

	post = models.ManyToManyField("posts.Post", blank=True, related_name='item_good')
	item_comment = models.ManyToManyField("posts.PostComment", blank=True, related_name='comment_good')
	photo_comment = models.ManyToManyField('gallery.PhotoComment', blank=True, related_name='gallery_comment_good')
	good_comment = models.ManyToManyField('goods.GoodComment', blank=True, related_name='good_comment_good')
	video_comment = models.ManyToManyField('video.VideoComment', blank=True, related_name='video_comment_good')
	message = models.ManyToManyField('chat.Message', blank=True, related_name='message_good')

	def __str__(self):
		return self.title

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	@classmethod
	def create_good(cls, image, title, sub_category, creator, description, \
					price, comments_enabled, votes_on, status):
		good = Good.objects.create(title=title, sub_category=sub_category, image=image, creator=creator, description=description, \
								status=status,price=price,comments_enabled=comments_enabled,votes_on=votes_on)
		channel_layer = get_channel_layer()
		payload = {
			"type": "receive",
			"key": "additional_post",
			"actor_name": good.creator.get_full_name()
			}
		async_to_sync(channel_layer.group_send)('notifications', payload)
		return good

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name="Товар"
		verbose_name_plural="Товары"
		ordering = ["-created"]

	def notification_user_repost(self, user):
		good_notification_handler(user, self.creator, good=self, verb=GoodNotify.REPOST)
	def notification_user_like(self, user):
		good_notification_handler(user, self.creator, good=self, verb=GoodNotify.LIKE)
	def notification_user_dislike(self, user):
		good_notification_handler(user, self.creator, good=self, verb=GoodNotify.DISLIKE)

	def notification_community_repost(self, user, community):
		good_community_notification_handler(creator=user, community=self.community, good=self, verb=GoodCommunityNotify.REPOST)
	def notification_community_like(self, user, community):
		good_community_notification_handler(creator=user, community=self.community, good=self, verb=GoodCommunityNotify.LIKE)
	def notification_community_dislike(self, user, community):
		good_community_notification_handler(creator=user, community=self.community, good=self, verb=GoodCommunityNotify.DISLIKE)

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
		comments_query = Q(good_comment_id=self.pk)
		comments_query.add(Q(parent_comment__isnull=True), Q.AND)
		return GoodComment.objects.filter(comments_query)
	def count_comments(self):
		parent_comments = GoodComment.objects.filter(good_comment_id=self.pk)
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



class GoodComment(models.Model):
	id = models.BigAutoField(primary_key=True)
	parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='good_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
	text = models.TextField(blank=True,null=True)
	is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
	is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
	good_comment = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)

	class Meta:
		indexes = (BrinIndex(fields=['created']), )
		verbose_name = "комментарий к записи"
		verbose_name_plural = "комментарии к записи"

	def __str__(self):
		return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

	def notification_user_comment(self, user):
		good_comment_notification_handler(creator=user, recipient=self.commenter, comment=self, verb=GoodNotify.POST_COMMENT, key='social_update')
	def notification_user_comment_like(self, user):
		good_comment_notification_handler(creator=user, recipient=self.commenter, comment=self, verb=GoodNotify.LIKE_COMMENT, key='social_update')
	def notification_user_comment_dislike(self, user):
		good_comment_notification_handler(creator=user, recipient=self.commenter, comment=self, verb=GoodNotify.DISLIKE_COMMENT, key='social_update')

	def notification_user_reply_comment(self, user):
		good_reply_notification_handler(creator=user, recipient=self.commenter, reply=self, verb=GoodNotify.POST_COMMENT_REPLY, key='social_update')
	def notification_user_like_reply(self, user):
		good_reply_notification_handler(creator=user, recipient=self.commenter, reply=self, verb=GoodNotify.LIKE_REPLY_COMMENT, key='social_update')
	def notification_user_dislike_reply(self, user):
		good_reply_notification_handler(creator=user, recipient=self.commenter, reply=self, verb=GoodNotify.DISLIKE_REPLY_COMMENT, key='social_update')

	def notification_community_comment(self, user, community):
		good_comment_community_notification_handler(creator=user, community=community, comment=self, verb=GoodCommunityNotify.POST_COMMENT, key='social_update')
	def notification_community_comment_like(self, user, community):
		good_comment_community_notification_handler(creator=user, community=community, comment=self, verb=GoodCommunityNotify.LIKE_COMMENT, key='social_update')
	def notification_community_comment_dislike(self, user, community):
		good_comment_community_notification_handler(creator=user, community=community, comment=self, verb=GoodCommunityNotify.DISLIKE_COMMENT, key='social_update')

	def notification_community_reply_comment(self, user, community):
		good_reply_community_notification_handler(creator=user, community=community, reply=self, verb=GoodNotify.POST_COMMENT_REPLY,  key='social_update')
	def notification_community_like_reply(self, user, community):
		good_reply_community_notification_handler(creator=user, community=community, reply=self, verb=GoodNotify.LIKE_REPLY_COMMENT,  key='social_update')
	def notification_community_dislike_reply(self, user, community):
		good_reply_community_notification_handler(creator=user, community=community, reply=self, verb=GoodNotify.DISLIKE_REPLY_COMMENT,  key='social_update')

	def get_replies(self):
		get_comments = GoodComment.objects.filter(parent_comment=self).all()
		return get_comments

	def count_replies(self):
		return self.good_comment_replies.count()

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
	def create_comment(cls, commenter, good_comment=None, parent_comment=None, text=None, created=None ):
		comment = GoodComment.objects.create(commenter=commenter, parent_comment=parent_comment, good_comment=good_comment, text=text)
		channel_layer = get_channel_layer()
		payload = {
			"type": "receive",
			"key": "comment_photo",
			"actor_name": comment.commenter.get_full_name()
			}
		async_to_sync(channel_layer.group_send)('notifications', payload)
		comment.save()
		return comment

	def get_created(self):
		from django.contrib.humanize.templatetags.humanize import naturaltime
		return naturaltime(self.created)

	def count_replies_ru(self):
		count = self.good_comment_replies.count()
		a = count % 10
		b = count % 100
		if (a == 1) and (b != 11):
			return str(count) + " ответ"
		elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
			return str(count) + " ответа"
		else:
			return str(count) + " ответов"
