import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.indexes import BrinIndex
from notifications.model.item import *
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from django.db.models import Count
from common.model.votes import PostVotes, PostCommentVotes
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit, ResizeToFill
from rest_framework.exceptions import ValidationError


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, related_name='items', on_delete=models.CASCADE, verbose_name="Создатель")
    is_closed = models.BooleanField(default=False, verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_repost = models.BooleanField(verbose_name="Это репост", default=False)
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

    item_attach = models.ManyToManyField("self", blank=True, related_name='attached_item')
    comment_attach = models.ManyToManyField("main.ItemComment", blank=True, related_name='attached_comment')

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="запись"
        verbose_name_plural="записи"


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
        likes = PostCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = PostCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes[0:6]

    def get_likes_for_comment_item(self, user):
        reactions_query = user._make_get_votes_query_comment(comment=self)
        return PostCommentVotes.objects.filter(item=self, vote__gt=0).filter(reactions_query)

    def get_dislikes_for_comment_item(self, user):
        reactions_query = user._make_get_votes_query_comment(comment=self)
        return PostCommentVotes.objects.filter(item=self, vote__lt=0).filter(reactions_query)

    def __str__(self):
        return str(self.item)

    def notification_user_comment(self, user):
        item_notification_handler(user, self.commenter, verb=ItemNotification.POST_COMMENT, comment=self, item=self.item, key='social_update')

    def notification_user_reply_comment(self, user):
        item_notification_handler(user, self.commenter, verb=ItemNotification.POST_COMMENT_REPLY, item=self.parent_comment.item, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        item_notification_handler(actor=user, recipient=self.commenter, verb=ItemNotification.LIKE_COMMENT, item=self.item, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        item_notification_handler(actor=user, recipient=self.commenter, verb=ItemNotification.DISLIKE_COMMENT, item=self.item, comment=self, key='social_update')

    def notification_community_comment(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.item.community, item=self.item, verb=ItemCommunityNotification.POST_COMMENT, comment=self, key='social_update')

    def notification_community_reply_comment(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.parent_comment.item.community, item=self.parent_comment.item, verb=ItemCommunityNotification.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')

    def notification_community_comment_like(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.item.community, verb=ItemCommunityNotification.LIKE_COMMENT, comment=self, item=self.item, key='social_update')

    def notification_community_comment_dislike(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.item.community, verb=ItemCommunityNotification.DISLIKE_COMMENT, comment=self, item=self.item, key='social_update')

    @classmethod
    def create_comment(cls, commenter, item, parent_comment, text):

        comment = ItemComment.objects.create(commenter=commenter, parent_comment=parent_comment, item=item, text=text, created=timezone.now())
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "comment_item",
            "actor_name": comment.commenter.get_full_name()
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        comment.save()
        return comment
