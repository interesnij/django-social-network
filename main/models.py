import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.indexes import BrinIndex
from django.db import transaction
from notifications.models import Notification, notification_handler
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from django.db.models import Count
from common.models import LikeDislike


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
    parent = models.ForeignKey("self", blank=True,
        null=True, on_delete=models.CASCADE, related_name="thread")
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
    votes = models.ForeignKey(LikeDislike, on_delete=models.CASCADE, null=True, related_query_name='items_vote')

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

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def likes_count(self):
        return likes.count()

    def dislikes_count(self):
        return dislikes.count()

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

    def notification_repost(self, user):
        notification_handler(user, self.creator,Notification.REPOST, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_like(self, user):
        notification_handler(user, self.creator,Notification.LIKED, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_dislike(self, user):
        notification_handler(user, self.creator,Notification.DISLIKED, action_object=self,id_value=str(self.uuid),key='social_update')


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


class ItemComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='post_comments')
    votes = models.OneToOneField(LikeDislike, on_delete=models.CASCADE, null=True, related_query_name='comments')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def get_replies(self):
        get_comments = ItemComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.count()

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def notification_comment(self, user):
        notification_handler(user, self.commenter,Notification.POST_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_reply_comment(self, user):
        notification_handler(user, self.commenter,Notification.POST_COMMENT_REPLY, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_comment_like(self, user):
        notification_handler(user, self.creator,Notification.LIKE_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_comment_dislike(self, user):
        notification_handler(user, self.creator,Notification.DISLIKE_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')


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


class TopPost(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='top_post')
    created = models.DateTimeField(editable=False, db_index=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        return super(TopPost, self).save(*args, **kwargs)
