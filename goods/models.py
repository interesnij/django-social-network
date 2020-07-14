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

class Good(models.Model):
	STATUS_DRAFT = 'D'
	STATUS_SOLD = 'S'
	STATUS_PUBLISHED = 'P'
	STATUSES = (
		(STATUS_DRAFT, 'Отложен'),
		(STATUS_PUBLISHED, 'Опубликован'),
		(STATUS_SOLD, 'Продан'),
		)

	uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
	title = models.CharField(max_length=200, verbose_name="Название")
	sub_category = models.ForeignKey(GoodSubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
	price = models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена товара")
	description = models.TextField(max_length=1000, verbose_name="Описание товара")
	community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, blank=True, verbose_name="Сообщество")
	comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
	votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_creator", on_delete=models.CASCADE, verbose_name="Создатель")
	is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
	is_hide = models.BooleanField(default=False, verbose_name="Товар виден только Вам")
	id = models.BigAutoField(primary_key=True)

	image = ProcessedImageField(verbose_name='Главное изображение', format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512,512)],upload_to="goods/%Y/%m/%d")
	image2 = ProcessedImageField(verbose_name='изображение 2', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFill(512, 512)],upload_to="goods/%Y/%m/%d")
	image3 = ProcessedImageField(verbose_name='изображение 3', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to="goods/%Y/%m/%d")
	image4 = ProcessedImageField(verbose_name='изображение 4', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to="goods/%Y/%m/%d")
	image5 = ProcessedImageField(verbose_name='изображение 5', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to="goods/%Y/%m/%d")
	status = models.CharField(choices=STATUSES, default=STATUS_PUBLISHED, max_length=2, verbose_name="Статус")
	item = models.ManyToManyField("posts.Post", blank=True, related_name='item_good')
	item_comment = models.ManyToManyField("posts.PostComment", blank=True, related_name='comment_good')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		channel_layer = get_channel_layer()
		payload = {"type": "receive","key": "additional_post","actor_name": self.creator.get_full_name()}
		async_to_sync(channel_layer.group_send)('notifications', payload)

	class Meta:
		indexes = (BrinIndex(fields=['created']),)
		verbose_name="Товар"
		verbose_name_plural="Товары"

	def notification_user_repost(self, user):
		good_notification_handler(user, self.creator, verb=GoodNotify.REPOST, key='social_update', good=self, comment=None)
	def notification_user_like(self, user):
		good_notification_handler(user, self.creator, verb=GoodNotify.LIKE, key='social_update', good=self, comment=None)
	def notification_user_dislike(self, user):
		good_notification_handler(user, self.creator, verb=GoodNotify.DISLIKE, key='social_update', good=self, comment=None)
	def notification_community_repost(self, user, community):
		good_community_notification_handler(actor=user, recipient=None, verb=GoodNotify.REPOST, key='social_update', community=self.community, good=self, comment=None)
	def notification_community_like(self, user, community):
		good_community_notification_handler(actor=user, recipient=None, verb=GoodNotify.LIKE, key='social_update', community=community, good=self, comment=None)
	def notification_community_dislike(self, user, community):
		good_community_notification_handler(actor=user, recipient=None, verb=GoodNotify.DISLIKE, key='social_update', community=community, good=self, comment=None)

	def likes(self):
		likes = GoodVotes.objects.filter(parent=self, vote__gt=0)
		return likes

	def window_likes(self):
		likes = GoodVotes.objects.filter(parent=self, vote__gt=0)
		return likes[0:6]

	def dislikes(self):
		dislikes = GoodVotes.objects.filter(parent=self, vote__lt=0)
		return dislikes
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
		comments_query = Q(photo_comment_id=self.pk)
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


class GoodComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='good_comment_replies', blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    good_comment = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = "комментарий к записи"
        verbose_name_plural = "комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def notification_user_comment(self, user):
        good_notification_handler(user, self.commenter, verb=GoodNotify.POST_COMMENT, comment=self, good=self.good_comment, key='social_update')
    def notification_user_reply_comment(self, user):
        good_notification_handler(user, self.commenter, verb=GoodNotify.POST_COMMENT_REPLY, good=self.parent_comment.good_comment, comment=self.parent_comment, key='social_update')
    def notification_user_comment_like(self, user):
        good_notification_handler(actor=user, recipient=self.commenter, verb=GoodNotify.LIKE_COMMENT, good=self.good_comment, comment=self, key='social_update')
    def notification_user_comment_dislike(self, user):
        good_notification_handler(actor=user, recipient=self.commenter, verb=GoodNotify.DISLIKE_COMMENT, good=self.good_comment, comment=self, key='social_update')
    def notification_community_comment(self, user, community):
        good_community_notification_handler(actor=user, recipient=None, community=community, good=self.good_comment, verb=GoodNotify.POST_COMMENT, comment=self, key='social_update')
    def notification_community_reply_comment(self, user, community):
        good_community_notification_handler(actor=user, recipient=None, community=community, good=self.good_comment.photo_comment, verb=GoodNotify.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')
    def notification_community_comment_like(self, user, community):
        good_community_notification_handler(actor=user, recipient=None, community=community, verb=GoodNotify.LIKE_COMMENT, comment=self, good=self.good_comment, key='social_update')
    def notification_community_comment_dislike(self, user, community):
        good_community_notification_handler(actor=user, recipient=None, community=community, verb=GoodNotify.DISLIKE_COMMENT, comment=self, good=self.good_comment, key='social_update')

    def get_replies(self):
        get_comments = GoodComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.good_comment_replies.count()

    def likes(self):
        likes = GoodCommentVotes.objects.filter(good_id=self.pk, vote__gt=0)
        return likes

    def window_likes(self):
        likes = GoodCommentVotes.objects.filter(good_id=self.pk, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = GoodCommentVotes.objects.filter(good_id=self.pk, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = GoodCommentVotes.objects.filter(good_id=self.pk, vote__lt=0)
        return dislikes[0:6]
    def likes_count(self):
	    likes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__gt=0).values("pk")
	    return likes.count()

    def dislikes_count(self):
	    dislikes = GoodCommentVotes.objects.filter(item_id=self.pk, vote__lt=0).values("pk")
	    return dislikes.count()
    def __str__(self):
	    return str(self.good)

    @classmethod
    def create_comment(cls, commenter, good=None, parent_comment=None, text=None, created=None ):
        comment = GoodComment.objects.create(commenter=commenter, parent_comment=parent_comment, good=good, text=text)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "comment_photo",
                "actor_name": comment.commenter.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        comment.save()
        return comment
