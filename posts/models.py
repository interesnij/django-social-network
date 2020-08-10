import uuid
from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from notify.model.item import *
from common.model.votes import PostVotes, PostCommentVotes


class Post(models.Model):
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
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    community = models.ForeignKey('communities.Community', related_name='post_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="thread")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    status = models.CharField(choices=STATUSES, default=STATUS_PUBLISHED, max_length=2, verbose_name="Статус статьи")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")

    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")

    @classmethod
    def create_post(cls, creator, text, community, comments_enabled, is_signature, status):
        post = Post.objects.create(creator=creator, text=text, community=community, is_signature=is_signature, comments_enabled=comments_enabled, status=status, )
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "additional_post",
            "actor_name": post.creator.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return post

    class Meta:
        ordering = ["-created"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

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
        item_notification_handler(user, self.creator, verb=ItemNotify.REPOST, key='social_update', item=self, comment=None)

    def notification_user_like(self, user):
        item_notification_handler(user, self.creator, verb=ItemNotify.LIKE, key='social_update', item=self, comment=None)

    def notification_user_dislike(self, user):
        item_notification_handler(user, self.creator, verb=ItemNotify.DISLIKE, key='social_update', item=self, comment=None)

    def notification_community_repost(self, user):
        item_community_notification_handler(actor=user, recipient=None, verb=ItemCommunityNotify.REPOST, key='social_update', community=self.community, item=self, comment=None)

    def notification_community_like(self, user):
        item_community_notification_handler(actor=user, recipient=None, verb=ItemCommunityNotify.LIKE, key='social_update', community=self.community, item=self, comment=None)

    def notification_community_dislike(self, user):
        item_community_notification_handler(actor=user, recipient=None, verb=ItemCommunityNotify.DISLIKE, key='social_update', community=self.community, item=self, comment=None)

    def get_comments(self):
        comments_query = Q(post_id=self.pk)
        comments_query.add(Q(parent_comment__isnull=True), Q.AND)
        return PostComment.objects.filter(comments_query)

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

    def likes(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def dislikes(self):
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def likes_count(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0).values("pk")
        return likes.count()

    def dislikes_count(self):
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0).values("pk")
        return dislikes.count()

    def window_likes(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

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

    def get_visiter_sity(self):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import OneUserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        sities = OneUserLocation.objects.filter(user_id__in=ids).distinct('city_ru')
        return sities

    def get_sity_count(self, sity):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import OneUserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        count = OneUserLocation.objects.filter(user_id__in=ids, city_ru=sity).count()
        return count

    def post_visits_count(self):
        from stst.models import PostNumbers
        return PostNumbers.objects.filter(post=self.pk).values('pk').count()
    def post_ad_visits_count(self):
        from stst.models import PostAdNumbers
        return PostAdNumbers.objects.filter(post=self.pk).values('pk').count()
    def all_visits_count(self):
        return self.post_visits_count() + self.post_ad_visits_count()

class PostComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "комментарий к записи"
        verbose_name_plural = "комментарии к записи"

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

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

    def likes_count(self):
        likes = PostCommentVotes.objects.filter(item=self, vote__gt=0).values("pk")
        return likes.count()

    def dislikes_count(self):
        dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0).values("pk")
        return dislikes.count()

    def window_dislikes(self):
        dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes[0:6]

    def __str__(self):
        return self.commenter.get_full_name()

    def notification_user_comment(self, user):
        item_notification_handler(user, self.commenter, verb=ItemNotify.POST_COMMENT, comment=self, item=self.post, key='social_update')

    def notification_user_reply_comment(self, user):
        item_notification_handler(user, self.commenter, verb=ItemNotify.POST_COMMENT_REPLY, item=self.parent_comment.post, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        item_notification_handler(actor=user, recipient=self.commenter, verb=ItemNotify.LIKE_COMMENT, item=self.post, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        item_notification_handler(actor=user, recipient=self.commenter, verb=ItemNotify.DISLIKE_COMMENT, item=self.post, comment=self, key='social_update')

    def notification_community_comment(self, user, community):
        item_community_notification_handler(actor=user, recipient=None, community=community, item=self.post, verb=ItemCommunityNotify.POST_COMMENT, comment=self, key='social_update')
    def notification_community_reply_comment(self, user, community):
        item_community_notification_handler(actor=user, recipient=None, community=community, item=self.parent_comment.post, verb=ItemCommunityNotify.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')

    def notification_community_comment_like(self, user, community):
        item_community_notification_handler(actor=user, recipient=None, community=community, verb=ItemCommunityNotify.LIKE_COMMENT, comment=self, item=self.post, key='social_update')

    def notification_community_comment_dislike(self, user, community):
        item_community_notification_handler(actor=user, recipient=None, community=community, verb=ItemCommunityNotify.DISLIKE_COMMENT, comment=self, item=self.post, key='social_update')

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
