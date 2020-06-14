import uuid
from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from notifications.model.item import ItemNotification, item_notification_handler, item_community_notification_handler
from common.model.votes import PostVotes, PostCommentVotes



class Post(models.Model):
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, related_name='post_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_repost = models.BooleanField(verbose_name="Это репост", default=False)
    #moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='items')
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

    @classmethod
    def create_post(cls, creator, text, community, comments_enabled, status):
        post = Post.objects.create(creator=creator, text=text, community=community, comments_enabled=comments_enabled, status=status, )
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "additional_post",
            "actor_name": post.creator.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return post

    class Meta:
        ordering=["-created"]
        verbose_name="Запись"
        verbose_name_plural="Записи"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    def count_comments(self):
        parent_comments = PostComment.objects.filter(post_id=self.pk)
        parents_count = parent_comments.count()
        i = 0
        for comment in parent_comments:
            i = i + comment.count_replies()
        i = i + parents_count
        return i

    def __str__(self):
        return self.creator.get_full_name()

    def notification_user_repost(self, user):
        item_notification_handler(user, self.creator, verb=ItemNotification.REPOST, key='social_update', item=self, comment=None)

    def notification_user_like(self, user):
        item_notification_handler(user, self.creator, verb=ItemNotification.LIKE, key='social_update', item=self, comment=None)

    def notification_user_dislike(self, user):
        item_notification_handler(user, self.creator, verb=ItemNotification.DISLIKE, key='social_update', item=self, comment=None)

    def notification_community_repost(self, user):
        item_community_notification_handler(actor=user, recipient=None, verb=ItemCommunityNotification.REPOST, key='social_update', community=self.community, item=self, comment=None)

    def notification_community_like(self, user):
        item_community_notification_handler(actor=user, recipient=None, verb=ItemCommunityNotification.LIKE, key='social_update', community=self.community, item=self, comment=None)

    def notification_community_dislike(self, user):
        item_community_notification_handler(actor=user, recipient=None, verb=ItemCommunityNotification.DISLIKE, key='social_update', community=self.community, item=self, comment=None)

    def get_comments(self):
        comments_query = Q(post_id=self.pk)
        comments_query.add(Q(parent_comment__isnull=True), Q.AND)
        comments_query.add(Q(is_deleted=False), Q.AND)
        return PostComment.objects.filter(comments_query)

    def likes(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

    def get_fixed_for_user(self, user_id):
        try:
            item = Post.objects.get(creator__id=user_id,is_fixed=True)
            item.is_fixed = False
            item.save(update_fields=['is_fixed'])
            new_fixed = Post.objects.get(creator__id=user_id,id=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])
        except:
            new_fixed = Post.objects.get(creator__id=user_id,id=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])

    def get_fixed_for_community(self, community_id):
        try:
            item = Post.objects.get(community__id=community_id,is_fixed=True)
            item.is_fixed = False
            item.save(update_fields=['is_fixed'])
            new_fixed = Post.objects.get(pk=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])
        except:
            new_fixed = Post.objects.get(community__id=community_id,id=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])

    def dislikes(self):
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes[0:6]

    def get_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents

    def get_window_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents[0:6]

    def count_reposts(self):
        parents = self.get_reposts()
        count_reposts = parents.count()
        return count_reposts

    def get_likes_for_item(self, user):
        reactions_query = user._make_get_votes_query(post=self)
        return PostVotes.objects.filter(parent=self, vote__gt=0).filter(reactions_query)

    def get_dislikes_for_item(self, user):
        reactions_query = user._make_get_votes_query(post=self)
        return PostVotes.objects.filter(parent=self, vote__lt=0).filter(reactions_query)

    def get_visiter_users(self):
        from stst.models import ItemNumbers
        from users.model.profile import OneUserLocation

        v_s = ItemNumbers.objects.filter(item=self.pk).values('user')
        ids = [use['user'] for use in v_s]
        sities = OneUserLocation.objects.filter(user_id__in=ids).distinct('city_ru')
        return sities

    def get_sity_count(self, sity):
        from stst.models import ItemNumbers
        from users.model.profile import OneUserLocation

        v_s = ItemNumbers.objects.filter(item=self.pk).values('user')
        ids = [use['user'] for use in v_s]
        count = OneUserLocation.objects.filter(user_id__in=ids, city_ru=sity).count()
        return count

    def all_visits_count(self):
        from stst.models import ItemNumbers
        return ItemNumbers.objects.filter(item=self.pk).values('pk').count()


class PostComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    #moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='post_comments')

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def get_replies(self):
        get_comments = PostComment.objects.filter(parent_comment=self).all()
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
        item_notification_handler(user, self.commenter, verb=ItemNotification.POST_COMMENT, comment=self, item=self.post, key='social_update')

    def notification_user_reply_comment(self, user):
        item_notification_handler(user, self.commenter, verb=ItemNotification.POST_COMMENT_REPLY, post=item.parent_comment.post, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        item_notification_handler(actor=user, recipient=self.commenter, verb=ItemNotification.LIKE_COMMENT, item=self.post, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        item_notification_handler(actor=user, recipient=self.commenter, verb=ItemNotification.DISLIKE_COMMENT, item=self.post, comment=self, key='social_update')

    def notification_community_comment(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.item.community, item=self.post, verb=ItemCommunityNotification.POST_COMMENT, comment=self, key='social_update')

    def notification_community_reply_comment(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.parent_comment.post.community, item=self.parent_comment.post, verb=ItemCommunityNotification.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')

    def notification_community_comment_like(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.post.community, verb=ItemCommunityNotification.LIKE_COMMENT, comment=self, item=self.item, key='social_update')

    def notification_community_comment_dislike(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.post.community, verb=ItemCommunityNotification.DISLIKE_COMMENT, comment=self, item=self.item, key='social_update')

    @classmethod
    def create_comment(cls, commenter, post, parent_comment, text):

        comment = PostComment.objects.create(commenter=commenter, parent_comment=parent_comment, post=post, text=text, created=timezone.now())
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "comment_item",
            "actor_name": comment.commenter.get_full_name()
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        comment.save()
        return comment
