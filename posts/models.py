import uuid
from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from notify.model.post import *
from common.model.votes import PostVotes, PostCommentVotes
from common.utils import try_except


class Post(models.Model):
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_MESSAGE_PUBLISHED = 'MP'
    STATUS_PUBLISHED = 'P'
    STATUS_ARHIVED = 'A'

    PHOTO_REPOST = 'C'
    PHOTO_ALBUM_REPOST = 'PAR'
    GOOD_REPOST = 'GR'
    MUSIC_REPOST = 'MR'
    MUSIC_LIST_REPOST = 'MLR'
    DOC_REPOST = 'DR'
    DOC_LIST_REPOST = 'DLR'
    VIDEO_REPOST = 'VR'
    VIDEO_LIST_REPOST = 'VLR'
    USER_REPOST = 'UR'
    COMMUNITY_REPOST = 'CR'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликована'),
        (STATUS_MESSAGE_PUBLISHED, 'Репост в сообщения'),
        (STATUS_ARHIVED, 'Архивирована'),

        (PHOTO_REPOST, 'Репост фотографии'),
        (PHOTO_ALBUM_REPOST, 'Репост фотоальбома'),
        (GOOD_REPOST, 'Репост товара'),
        (MUSIC_REPOST, 'Репост аудиозаписи'),
        (MUSIC_LIST_REPOST, 'Репост плейлиста аудиозаписей'),
        (DOC_REPOST, 'Репост документа'),
        (DOC_LIST_REPOST, 'Репост списка документов'),
        (VIDEO_REPOST, 'Репост видеозаписи'),
        (VIDEO_LIST_REPOST, 'Репост списка видеозаписей'),
        (USER_REPOST, 'Репост пользователя'),
        (COMMUNITY_REPOST, 'Репост сообщества'),
    )
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    community = models.ForeignKey('communities.Community', related_name='post_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="thread")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    status = models.CharField(choices=STATUSES, default=STATUS_PUBLISHED, max_length=5, verbose_name="Статус статьи")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")

    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")

    @classmethod
    def create_post(cls, creator, text, community, parent, comments_enabled, is_signature, status):
        post = Post.objects.create(creator=creator, text=text, parent=parent, community=community, is_signature=is_signature, comments_enabled=comments_enabled, status=status, )
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "additional_post",
            "actor_name": post.creator.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return post
    @classmethod
    def create_parent_post(cls, creator, community, status):
        post = cls.objects.create(creator=creator, community=community, status=status, )
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

    def get_parent_attach_photos(self):
        return self.parent.item_photo.all()
    def get_parent_attach_photo_list(self):
        return self.parent.post_album.all()
    def get_parent_attach_videos(self):
        return self.parent.item_video.all()
    def get_parent_attach_video_list(self):
        return self.parent.post_video_album.all()
    def get_parent_attach_goods(self):
        return self.parent.item_good.all()
    def get_parent_attach_articles(self):
        return self.parent.attached_item.all()
    def get_parent_attach_tracks(self):
        return self.parent.item_music.all()
    def get_parent_attach_music_list(self):
        return self.parent.post_soundlist.all()
    def get_parent_attach_docs(self):
        return self.parent.item_doc.all()
    def get_parent_attach_doc_list(self):
        return self.parent.post_doclist.all()

    def get_attach_photos(self):
        return self.item_photo.all()
    def get_attach_photo_list(self):
        return self.post_album.all()
    def get_attach_videos(self):
        return self.item_video.all()
    def get_attach_video_list(self):
        return self.post_video_album.all()
    def get_attach_goods(self):
        return self.item_good.all()
    def get_attach_articles(self):
        return self.attached_item.all()
    def get_attach_tracks(self):
        return self.item_music.all()
    def get_attach_music_list(self):
        return self.post_soundlist.all()
    def get_attach_docs(self):
        return self.item_doc.all()
    def get_attach_doc_list(self):
        return self.post_doclist.all()

    def is_photo_list_attached(self):
        return self.post_album.filter(post__pk=self.pk).exists()
    def is_playlist_attached(self):
        return self.post_soundlist.filter(post__pk=self.pk).exists()
    def is_video_list_attached(self):
        return self.post_video_album.filter(post__pk=self.pk).exists()
    def is_good_list_attached(self):
        return self.post_good_album.filter(post__pk=self.pk).exists()
    def is_doc_list_attached(self):
        return self.post_doclist.filter(post__pk=self.pk).exists()

    def get_u_attach_items(self):
        if self.is_photo_list_attached():
            return "generic/attach/u_photo_list_attach.html"
        elif self.is_playlist_attached():
            return "generic/attach/u_playlist_attach.html"
        elif self.is_video_list_attached():
            return "generic/attach/u_video_list_attach.html"
        elif self.is_good_list_attached():
            return "generic/attach/u_good_list_attach.html"
        elif self.is_doc_list_attached():
            return "generic/attach/u_doc_list_attach.html"
        else:
            return "generic/attach/u_post_attach.html"

    def get_c_attach_items(self):
        if self.is_photo_list_attached():
            return "generic/attach/c_photo_list_attach.html"
        elif self.is_playlist_attached():
            return "generic/attach/c_playlist_attach.html"
        elif self.is_video_list_attached():
            return "generic/attach/c_video_list_attach.html"
        elif self.is_good_list_attached():
            return "generic/attach/c_good_list_attach.html"
        elif self.is_doc_list_attached():
            return "generic/attach/c_doc_list_attach.html"
        else:
            return "generic/attach/c_post_attach.html"

    def is_photo_repost(self):
        return try_except(self.status == Post.PHOTO_REPOST)
    def get_photo_repost(self):
        photo = self.parent.item_photo.all()[0]
        return photo
    def is_photo_album_repost(self):
        return try_except(self.status == Post.PHOTO_ALBUM_REPOST)
    def get_photo_album_repost(self):
        photo_album = self.parent.post_album.all()[0]
        return photo_album

    def is_music_repost(self):
        return try_except(self.status == Post.MUSIC_REPOST)
    def is_music_list_repost(self):
        return try_except(self.status == Post.MUSIC_LIST_REPOST)
    def get_playlist_repost(self):
        playlist = self.parent.post_soundlist.all()[0]
        return playlist
    def get_music_repost(self):
        music = self.parent.item_music.all()[0]
        return music

    def is_good_repost(self):
        return try_except(self.status == Post.GOOD_REPOST)

    def is_doc_repost(self):
        return try_except(self.status == Post.DOC_REPOST)
    def is_doc_list_repost(self):
        return try_except(self.status == Post.DOC_LIST_REPOST)
    def get_doc_list_repost(self):
        list = self.parent.post_doclist.all()[0]
        return list
    def get_doc_repost(self):
        doc = self.parent.item_doc.all()[0]
        return doc

    def is_video_repost(self):
        return try_except(self.status == Post.VIDEO_REPOST)
    def is_video_list_repost(self):
        return try_except(self.status == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        video_list = self.parent.post_video_album.all()[0]
        return video_list

    def is_user_repost(self):
        return try_except(self.status == Post.USER_REPOST)
    def is_community_repost(self):
        return try_except(self.status == Post.COMMUNITY_REPOST)

    def get_c_post_parent(self):
        parent = self.parent
        if parent.is_photo_repost():
            return "post_community/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "post_community/photo_album_repost.html"
        elif parent.is_good_repost():
            return "post_community/good_repost.html"
        elif parent.is_music_repost():
            return "post_community/music_repost.html"
        elif parent.is_music_list_repost():
            return "post_community/music_list_repost.html"
        elif parent.is_video_repost():
            return "post_community/video_repost.html"
        elif parent.is_video_list_repost():
            return "post_community/video_list_repost.html"
        elif parent.is_doc_repost():
            return "post_community/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "post_community/doc_list_repost.html"
        elif parent.is_user_repost():
            return "post_community/user_repost.html"
        elif parent.is_community_repost():
            return "post_community/community_repost.html"
        else:
            return "generic/attach/parent_community.html"

    def get_u_post_parent(self):
        parent = self.parent
        if parent.is_photo_repost():
            return "post_user/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "post_user/photo_album_repost.html"
        elif parent.is_good_repost():
            return "post_user/good_repost.html"
        elif parent.is_music_repost():
            return "post_user/music_repost.html"
        elif parent.is_music_list_repost():
            return "post_user/music_list_repost.html"
        elif parent.is_video_repost():
            return "post_user/video_repost.html"
        elif parent.is_video_list_repost():
            return "post_user/video_list_repost.html"
        elif parent.is_doc_repost():
            return "post_user/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "post_user/doc_list_repost.html"
        elif parent.is_user_repost():
            return "post_user/user_repost.html"
        elif parent.is_community_repost():
            return "post_user/community_repost.html"
        else:
            return "generic/attach/parent_user.html"

    def get_u_news_parent(self):
        parent = self.parent
        if parent.is_photo_repost():
            return "u_posts/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "u_posts/photo_album_repost.html"
        elif parent.is_good_repost():
            return "u_posts/good_repost.html"
        elif parent.is_music_repost():
            return "u_posts/music_repost.html"
        elif parent.is_music_list_repost():
            return "u_posts/music_list_repost.html"
        elif parent.is_video_repost():
            return "u_posts/video_repost.html"
        elif parent.is_video_list_repost():
            return "u_posts/video_list_repost.html"
        elif parent.is_doc_repost():
            return "u_posts/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "u_posts/doc_list_repost.html"
        elif parent.is_user_repost():
            return "u_posts/user_repost.html"
        elif parent.is_community_repost():
            return "u_posts/community_repost.html"
        else:
            return "u_posts/parent_user.html"

    def get_c_news_parent(self):
        parent = self.parent
        if parent.is_photo_repost():
            return "c_posts/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "c_posts/photo_album_repost.html"
        elif parent.is_good_repost():
            return "c_posts/good_repost.html"
        elif parent.is_music_repost():
            return "c_posts/music_repost.html"
        elif parent.is_music_list_repost():
            return "c_posts/music_list_repost.html"
        elif parent.is_video_repost():
            return "c_posts/video_repost.html"
        elif parent.is_video_list_repost():
            return "c_posts/video_list_repost.html"
        elif parent.is_doc_repost():
            return "c_posts/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "c_posts/doc_list_repost.html"
        elif parent.is_user_repost():
            return "c_posts/user_repost.html"
        elif parent.is_community_repost():
            return "c_posts/community_repost.html"
        else:
            return "c_posts/parent_community.html"


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
        post_notification_handler(user, self.creator, verb=PostNotify.REPOST, key='social_update', post=self, comment=None)

    def notification_user_like(self, user):
        post_notification_handler(user, self.creator, verb=PostNotify.LIKE, key='social_update', post=self, comment=None)

    def notification_user_dislike(self, user):
        post_notification_handler(user, self.creator, verb=PostNotify.DISLIKE, key='social_update', post=self, comment=None)

    def notification_community_repost(self, user):
        post_community_notification_handler(actor=user, recipient=None, verb=PostCommunityNotify.REPOST, key='social_update', community=self.community, post=self, comment=None)

    def notification_community_like(self, user):
        post_community_notification_handler(actor=user, recipient=None, verb=PostCommunityNotify.LIKE, key='social_update', community=self.community, post=self, comment=None)

    def notification_community_dislike(self, user):
        post_community_notification_handler(actor=user, recipient=None, verb=PostCommunityNotify.DISLIKE, key='social_update', community=self.community, post=self, comment=None)

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
        post_notification_handler(user, self.commenter, verb=PostNotify.POST_COMMENT, comment=self, post=self.post, key='social_update')

    def notification_user_reply_comment(self, user):
        post_notification_handler(user, self.commenter, verb=PostNotify.POST_COMMENT_REPLY, post=self.parent_comment.post, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        post_notification_handler(actor=user, recipient=self.commenter, verb=PostNotify.LIKE_COMMENT, post=self.post, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        post_notification_handler(actor=user, recipient=self.commenter, verb=PostNotify.DISLIKE_COMMENT, post=self.post, comment=self, key='social_update')

    def notification_community_comment(self, user, community):
        post_community_notification_handler(actor=user, recipient=None, community=community, post=self.post, verb=PostCommunityNotify.POST_COMMENT, comment=self, key='social_update')
    def notification_community_reply_comment(self, user, community):
        post_community_notification_handler(actor=user, recipient=None, community=community, post=self.parent_comment.post, verb=PostCommunityNotify.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')

    def notification_community_comment_like(self, user, community):
        post_community_notification_handler(actor=user, recipient=None, community=community, verb=PostCommunityNotify.LIKE_COMMENT, comment=self, post=self.post, key='social_update')

    def notification_community_comment_dislike(self, user, community):
        post_community_notification_handler(actor=user, recipient=None, community=community, verb=PostCommunityNotify.DISLIKE_COMMENT, comment=self, post=self.post, key='social_update')

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

    def count_replies_ru(self):
        count = self.replies.count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def get_attach_photos(self):
        return self.comment_photo.all()
    def get_attach_videos(self):
        return self.comment_video.all()
    def get_attach_goods(self):
        return self.comment_good.all()
    def get_attach_articles(self):
        return self.attached_comment.all()
    def get_attach_tracks(self):
        return self.comment_music.all()
    def get_attach_docs(self):
        return self.comment_doc.all()
