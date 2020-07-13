from django.db import models
import uuid
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.model.good import *
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
	uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
	title = models.CharField(max_length=200, verbose_name="Название")
	sub_category = models.ForeignKey(GoodSubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
	price = models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена товара")
	description = models.TextField(max_length=1000, verbose_name="Описание товара")
	community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
	comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
	votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="good_creator", db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
	is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
	id = models.BigAutoField(primary_key=True)

	image = ProcessedImageField(verbose_name='Главное изображение', format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512,512)],upload_to="goods/%Y/%m/%d")
	image2 = ProcessedImageField(verbose_name='изображение 2', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFill(512, 512)],upload_to="goods/%Y/%m/%d")
	image3 = ProcessedImageField(verbose_name='изображение 3', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to="goods/%Y/%m/%d")
	image4 = ProcessedImageField(verbose_name='изображение 4', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to="goods/%Y/%m/%d")
	image5 = ProcessedImageField(verbose_name='изображение 5', blank=True, format='JPEG',options={'quality': 80}, processors=[ResizeToFit(512, 512)],upload_to="goods/%Y/%m/%d")

	STATUS_DRAFT = 'D'
	STATUS_SOLD = 'S'
	STATUS_PUBLISHED = 'P'
	STATUSES = (
		(STATUS_DRAFT, 'Отложен'),
		(STATUS_PUBLISHED, 'Опубликован'),
		(STATUS_SOLD, 'Продан'),
		)
	status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_PUBLISHED, max_length=2, verbose_name="Статус")
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
		good_notification_handler(user, self.creator, verb=GoodNotification.REPOST, key='social_update', good=self, comment=None)
	def notification_user_like(self, user):
		good_notification_handler(user, self.creator, verb=GoodNotification.LIKE, key='social_update', good=self, comment=None)
	def notification_user_dislike(self, user):
		good_notification_handler(user, self.creator, verb=GoodNotification.DISLIKE, key='social_update', good=self, comment=None)
	def notification_community_repost(self, user):
		good_community_notification_handler(actor=user, recipient=None, verb=GoodCommunityNotification.REPOST, key='social_update', community=self.community, good=self, comment=None)
	def notification_community_like(self, user):
		good_community_notification_handler(actor=user, recipient=None, verb=GoodCommunityNotification.LIKE, key='social_update', community=self.community, good=self, comment=None)
	def notification_community_dislike(self, user):
		good_community_notification_handler(actor=user, recipient=None, verb=GoodCommunityNotification.DISLIKE, key='social_update', community=self.community, good=self, comment=None)

	def get_comments(self, user):
		comments_query = self._make_get_comments_for_post_query(user=user)
		return GoodComment.objects.filter(comments_query)
	def get_comment_replies(self, post_comment_id):
		post_comment = GoodComment.objects.get(pk=post_comment_id)
		return self.get_comment_replies_for_comment_with_post(post_comment=post_comment)

	def get_comment_replies_for_comment_with_post(self, post_comment):
		comment_replies_query = self._make_get_comments_for_post_query(self, post_comment_parent_id=post_comment.pk)
		return GoodComment.objects.filter(comment_replies_query)

	def _make_get_comments_for_post_query(self, user, post_comment_parent_id=None):
		comments_query = Q(good_id=self.pk)
		if post_comment_parent_id is None:
			comments_query.add(Q(parent_comment__isnull=True), Q.AND)
		else:
			comments_query.add(Q(parent_comment__id=post_comment_parent_id), Q.AND)
		post_community = self.community
		if post_community:
			if not user.is_staff_of_community_with_name(community_name=post_community.name):
				blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=user.pk) | Q(commenter__user_blocks__blocked_user_id=user.pk))
				blocked_users_query_staff_members = Q(commenter__communities_memberships__community_id=post_community.pk)
				blocked_users_query_staff_members.add(Q(commenter__communities_memberships__is_administrator=True) | Q(commenter__communities_memberships__is_moderator=True), Q.AND)
				blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
				comments_query.add(blocked_users_query, Q.AND)
				#comments_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
		else:
			blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=user.pk) | Q(commenter__user_blocks__blocked_user_id=user.pk))
			comments_query.add(blocked_users_query, Q.AND)
			#comments_query.add(~Q(moderated_object__reports__reporter_id=user.pk), Q.AND)
			comments_query.add(Q(is_deleted=False), Q.AND)
		return comments_query

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


class GoodComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
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
        good_notification_handler(user, self.commenter, verb=GoodNotification.POST_COMMENT, comment=self, good=self.good, key='social_update')

    def notification_user_reply_comment(self, user):
        good_notification_handler(user, self.commenter, verb=GoodNotification.POST_COMMENT_REPLY, good=self.parent_comment.good, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        good_notification_handler(actor=user, recipient=None, verb=GoodNotification.LIKE_COMMENT, photo=self.good, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        good_notification_handler(actor=user, recipient=None, verb=GoodNotification.DISLIKE_COMMENT, good=self.good, comment=self, key='social_update')

    def notification_community_comment(self, user):
        good_community_notification_handler(actor=user, recipient=None, community=self.good.community, good=self.good, verb=GoodCommunityNotification.POST_COMMENT, comment=self, key='social_update')

    def notification_community_reply_comment(self, user):
        good_community_notification_handler(actor=user, recipient=None, community=self.parent_comment.good.community, good=self.parent_comment.good, verb=GoodCommunityNotification.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')

    def notification_community_comment_like(self, user):
        good_community_notification_handler(actor=user, recipient=None, community=self.good.community, verb=GoodCommunityNotification.LIKE_COMMENT, comment=self, good=self.good, key='social_update')

    def notification_community_comment_dislike(self, user):
        good_community_notification_handler(actor=user, recipient=None, community=self.good.community, verb=GoodCommunityNotification.DISLIKE_COMMENT, comment=self, good=self.good, key='social_update')

    def get_replies(self):
        get_comments = GoodComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.count()

    def likes(self):
        likes = GoodCommentVotes.objects.filter(good=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = GoodCommentVotes.objects.filter(good=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = GoodCommentVotes.objects.filter(good=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = GoodCommentVotes.objects.filter(good=self, vote__lt=0)
        return dislikes[0:6]

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
