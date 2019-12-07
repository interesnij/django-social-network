import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.indexes import BrinIndex
from django.db import transaction
from notifications.model.item import *
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from django.db.models import Count
from common.models import ItemVotes, ItemCommentVotes
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit, ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from rest_framework.exceptions import ValidationError


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, related_name='items', on_delete=models.CASCADE, verbose_name="Создатель")
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_closed = models.BooleanField(default=False, verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_repost = models.BooleanField(verbose_name="Это репост", default=False)
    views=models.IntegerField(default=0, verbose_name="Просмотры")
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='items')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="thread")
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_PUBLISHED = 'P'
    STATUS_ARHIVED = 'A'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликована'),
        (STATUS_ARHIVED, 'Архивирована'),
    )
    status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_PUBLISHED, max_length=2, verbose_name="Статус статьи")

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name="запись"
        verbose_name_plural="записи"

    def save(self, *args, **kwargs):
        if not self.is_fixed:
            return super(Item, self).save(*args, **kwargs)
        with transaction.atomic():
            Item.objects.filter(
                is_fixed=True).update(is_fixed=False)
            return super(Item, self).save(*args, **kwargs)

    def count_comments(self):
        parent_comments = ItemComment.objects.filter(item=self).count()
        return parent_comments

    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return self

    def get_thread(self):
        parent = self.get_parent()
        return parent.thread.all()

    def count_thread(self):
        return self.get_thread().count()

    def __str__(self):
        return "{0}/{1}".format(self.creator.get_full_name(), self.views)

    def notification_user_repost(self, user):
        item_notification_handler(user, self.creator, ItemNotification.REPOST, key='social_update', item=self, comment=None)

    def notification_user_like(self, user):
        item_notification_handler(user, self.creator, ItemNotification.LIKE, key='social_update', item=self, comment=None)

    def notification_user_dislike(self, user):
        item_notification_handler(user, self.creator, ItemNotification.DISLIKE, key='social_update', item=self, comment=None)

    def notification_community_repost(self, user):
        item_community_notification_handler(user, self.creator, ItemCommunityNotification.REPOST, key='social_update', item=self, comment=None)

    def notification_community_like(self, user):
        item_community_notification_handler(user, self.creator, ItemCommunityNotification.LIKE, key='social_update', item=self, comment=None)

    def notification_community_dislike(self, user):
        item_community_notification_handler(user, self.creator, ItemCommunityNotification.DISLIKE, key='social_update', item=self, comment=None)

    def get_comments(self, user):
        item = Item.objects.get(pk=self.pk)
        comments_query = self._make_get_comments_for_post_query(user=user)
        return ItemComment.objects.filter(comments_query)

    def get_comment_replies(self, post_comment_id):
        post_comment = ItemComment.objects.get(pk=post_comment_id)
        item = Item.objects.get(uuid=self.uuid)
        return item.get_comment_replies_for_comment_with_post(post_comment=post_comment)

    def get_comment_replies_for_comment_with_post(self, post_comment):
        comment_replies_query = self._make_get_comments_for_post_query(self, post_comment_parent_id=post_comment.pk)
        return ItemComment.objects.filter(comment_replies_query)

    def _make_get_comments_for_post_query(self, user, post_comment_parent_id=None):
        comments_query = Q(item_id=self.pk)

        if post_comment_parent_id is None:
            comments_query.add(Q(parent_comment__isnull=True), Q.AND)
        else:
            comments_query.add(Q(parent_comment__id=post_comment_parent_id), Q.AND)

        post_community = self.community

        if post_community:
            if not user.is_staff_of_community_with_name(community_name=post_community.name):
                blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=user.pk) | Q(
                    commenter__user_blocks__blocked_user_id=user.pk))
                blocked_users_query_staff_members = Q(
                    commenter__communities_memberships__community_id=post_community.pk)
                blocked_users_query_staff_members.add(Q(commenter__communities_memberships__is_administrator=True) | Q(
                    commenter__communities_memberships__is_moderator=True), Q.AND)
                blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
                comments_query.add(blocked_users_query, Q.AND)
                comments_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
        else:
            blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=user.pk) | Q(
                commenter__user_blocks__blocked_user_id=user.pk))
            comments_query.add(blocked_users_query, Q.AND)

        comments_query.add(~Q(moderated_object__reports__reporter_id=user.pk), Q.AND)
        comments_query.add(Q(is_deleted=False), Q.AND)
        return comments_query

    def likes(self):
        likes = ItemVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def dislikes(self):
        dislikes = ItemVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def get_likes_for_item(self, user):
        reactions_query = user._make_get_votes_query(item=self)
        return ItemVotes.objects.filter(parent=self, vote__gt=0).filter(reactions_query)

    def get_dislikes_for_item(self, user):
        reactions_query = user._make_get_votes_query(item=self)
        return ItemVotes.objects.filter(parent=self, vote__lt=0).filter(reactions_query)


class ItemComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='post_comments')
    item_comment_photo = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to='comment_photos/%Y/%m/%d', processors=[ResizeToFit(width=1024, upscale=False)])
    item_comment_photo2 = ProcessedImageField(format='JPEG', blank=True, options={'quality': 90}, upload_to='comment_photos/%Y/%m/%d', processors=[ResizeToFit(width=1024, upscale=False)])

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def get_replies(self):
        get_comments = ItemComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.count()

    def likes(self):
        likes = ItemCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes

    def dislikes(self):
        dislikes = ItemCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes

    def get_likes_for_comment_item(self, user):
        reactions_query = user._make_get_votes_query_comment(comment=self)
        return ItemCommentVotes.objects.filter(id=self.pk, vote__gt=0).filter(reactions_query)

    def get_dislikes_for_comment_item(self, user):
        reactions_query = user._make_get_votes_query_comment(comment=self)
        return ItemCommentVotes.objects.filter(id=self.pk, vote__lt=0).filter(reactions_query)

    def __str__(self):
        return str(self.item)

    def notification_user_comment(self, user):
        item_notification_handler(user, self.commenter, ItemNotification.POST_COMMENT, comment=self, item=self.item, key='social_update')

    def notification_user_reply_comment(self, user):
        item_notification_handler(user, self.commenter, ItemNotification.POST_COMMENT_REPLY, item=self.parent_comment.item, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        item_notification_handler(user, self.commenter, ItemNotification.LIKE_COMMENT, item=self.item, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        item_notification_handler(user, self.commenter, ItemNotification.DISLIKE_COMMENT, item=self.item, comment=self, key='social_update')

    def notification_community_comment(self, user):
        item_community_notification_handler(user, self.commenter, ItemCommunityNotification.POST_COMMENT, comment=self, item=self.item, key='social_update')

    def notification_community_reply_comment(self, user):
        item_community_notification_handler(user, self.commenter, ItemCommunityNotification.POST_COMMENT_REPLY, comment=self, item=self.item, key='social_update')

    def notification_community_comment_like(self, user):
        item_community_notification_handler(user, self.commenter, ItemCommunityNotification.LIKE_COMMENT, comment=self, item=self.item, key='social_update')

    def notification_community_comment_dislike(self, user):
        item_community_notification_handler(user, self.commenter, ItemCommunityNotification.DISLIKE_COMMENT, comment=self, item=self.item, key='social_update')

    @classmethod
    def create_user_comment(cls, commenter, item=None, parent_comment=None, community=None, text=None, item_comment_photo=None, item_comment_photo2=None, created=None ):
        comment = ItemComment.objects.create(commenter=commenter, parent_comment=parent_comment, item=item, text=text, item_comment_photo=item_comment_photo,item_comment_photo2=item_comment_photo2)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "comment_item",
                "actor_name": comment.commenter.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        comment.save()
        return comment


class ItemMute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='mutes')
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mutes')

    class Meta:
        unique_together = ('item', 'muter',)

    @classmethod
    def create_post_mute(cls, item_id, muter_id):
        return cls.objects.create(item_id=item_id, muter_id=muter_id)


class ItemCommentMute(models.Model):
    item_comment = models.ForeignKey(ItemComment, on_delete=models.CASCADE, related_name='mutes')
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mutes')

    class Meta:
        unique_together = ('item_comment', 'muter',)

    @classmethod
    def create_post_comment_mute(cls, post_comment_id, muter_id):
        return cls.objects.create(post_comment_id=post_comment_id, muter_id=muter_id)
