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
from common.utils import try_except


class Post(models.Model):
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_PUBLISHED = 'P'
    STATUS_ARHIVED = 'A'

    PHOTO_REPOST = 'C'
    PHOTO_ALBUM_REPOST = 'PAR'
    GOOD_REPOST = 'GR'
    MUSIC_REPOST = 'MR'
    MUSIC_LIST_REPOST = 'MLR'
    VIDEO_REPOST = 'VR'
    VIDEO_LIST_REPOST = 'VLR'
    USER_REPOST = 'UR'
    COMMUNITY_REPOST = 'CR'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликована'),
        (STATUS_ARHIVED, 'Архивирована'),

        (PHOTO_REPOST, 'Репост фотографии'),
        (PHOTO_ALBUM_REPOST, 'Репост фотоальбома'),
        (GOOD_REPOST, 'Репост товара'),
        (MUSIC_REPOST, 'Репост аудиозаписи'),
        (MUSIC_LIST_REPOST, 'Репост плейлиста аудиозаписей'),
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
    status = models.CharField(choices=STATUSES, default=STATUS_PUBLISHED, max_length=2, verbose_name="Статус статьи")
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

    def get_attach_photos(self):
        return self.parent.item_photo.all()
    def get_attach_videos(self):
        return self.parent.item_video.all()
    def get_attach_goods(self):
        return self.parent.item_good.all()
    def get_attach_articles(self):
        return self.parent.attached_item.all()
    def get_attach_tracks(self):
        return self.parent.item_music.all()

    def is_photo_repost(self):
        return try_except(self.parent.status == Post.PHOTO_REPOST)
    def get_c_photo_repost(self):
        photo = self.parent.item_photo.all()[0]
        pk = self.parent.community.pk
        return '<img photo-uuid="{}" data-pk="{}" class="c_WA_photo image_fit lazyload pointer" data-src="{}" alt="img">'.format(photo.uuid, pk, photo.file.url)
    def get_u_photo_repost(self):
        photo = self.parent.item_photo.all()[0]
        return '<img photo-uuid="{}" data-pk="{}" class="u_WA_photo image_fit lazyload pointer" data-src="{}" alt="img">'.format(photo.uuid, self.parent.creator.pk, photo.file.url)

    def is_photo_album_repost(self):
        return try_except(self.status == Post.PHOTO_ALBUM_REPOST)
    def get_photo_album_repost(self):
        photo_album = self.parent.post_alnum.all()[0]
        return photo_album

    def is_good_repost(self):
        return try_except(self.status == Post.GOOD_REPOST)
    def get_u_good_repost(self):
        good = self.parent.item_good.all()[0]
        badge = '<span class="badge badge-primary mb-2" style="position:absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M17.21 9l-4.38-6.56c-.19-.28-.51-.42-.83-.42-.32 0-.64.14-.83.43L6.79 9H2c-.55 0-1 .45-1 1 0 .09.01.18.04.27l2.54 9.27c.23.84 1 1.46 1.92 1.46h13c.92 0 1.69-.62 1.93-1.46l2.54-9.27L23 10c0-.55-.45-1-1-1h-4.79zM9 9l3-4.4L15 9H9zm3 8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>{}</span>'.format(photo.title)
        if good.image:
            image = good.image
        else:
            image = '<svg class="image_fit svg_default" style="width:100%;height:auto" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>'
        return '<div class="u_good_detail good pointer" good-uuid="{}" data-pk="{}">{badge}{image}</div>'.format(photo.uuid, photo.creator.pk, badge, image)
    def get_c_good_repost(self):
        good = self.parent.item_good.all()[0]
        badge = '<span class="badge badge-primary mb-2" style="position:absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M17.21 9l-4.38-6.56c-.19-.28-.51-.42-.83-.42-.32 0-.64.14-.83.43L6.79 9H2c-.55 0-1 .45-1 1 0 .09.01.18.04.27l2.54 9.27c.23.84 1 1.46 1.92 1.46h13c.92 0 1.69-.62 1.93-1.46l2.54-9.27L23 10c0-.55-.45-1-1-1h-4.79zM9 9l3-4.4L15 9H9zm3 8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>{}</span>'.format(photo.title)
        if good.image:
            image = good.image
        else:
            image = '<svg class="image_fit svg_default" style="width:100%;height:auto" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>'
        return '<div class="c_good_detail good pointer" good-uuid="{}" data-pk="{}">{badge}{image}</div>'.format(photo.uuid, photo.creator.pk, badge, image)

    def is_music_repost(self):
        return try_except(self.status == Post.MUSIC_REPOST)

    def get_music_repost(self):
        music = self.parent.item_music.all()[0]
        return music
    def is_music_list_repost(self):
        return try_except(self.status == Post.MUSIC_LIST_REPOST)
    def get_music_list_repost(self):
        music_list = self.parent.post_soundlist.all()[0]
        return music_list

    def is_video_repost(self):
        return try_except(self.status == Post.VIDEO_REPOST)
    def get_u_video_repost(self):
        video = self.parent.item_video.all()[0]
        return '<img class="image_fit lazyload" data-src="{}" alt="img"><div class="video_icon_play_v2 u_video_detail" data-pk="{}" data-uuid="{}" video-counter="0"></div>'.format(video.image.url, video.creator.pk, video.uuid)
    def get_u_video_repost(self):
        video = self.parent.item_video.all()[0]
        return '<img class="image_fit lazyload" data-src="{}" alt="img"><div class="video_icon_play_v2 c_video_detail" data-pk="{}" data-uuid="{}" video-counter="0"></div>'.format(video.image.url, video.creator.pk, video.uuid)

    def is_video_list_repost(self):
        return try_except(self.status == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        video_list = self.parent.post_video_album.all()[0]
        return video_list

    def is_user_repost(self):
        return try_except(self.status == Post.USER_REPOST)
    def is_community_repost(self):
        return try_except(self.status == Post.COMMUNITY_REPOST)

    def get_u_attach_items(self):
        if self.is_photo_repost():
            return self.get_u_photo_repost()
        elif self.is_photo_album_repost():
            return 'Пользователь поделился фотоальбомом!'
        elif self.is_good_repost():
            return self.get_u_good_repost()
        elif self.is_music_repost():
            return "Пользователь поделился music!"
        elif self.is_music_list_repost():
            return "Пользователь поделился плейлистом!"
        elif self.is_video_repost():
            return self.get_u_video_repost()
        elif self.is_video_list_repost():
            return "Пользователь поделился видео-альбомом!"
        elif self.is_user_repost():
            return "Пользователь поделился пользователем!"
        elif self.is_community_repost():
            return "Пользователь поделился сообществом!"
        else:
            return False

    def get_c_attach_items(self):
        if self.is_photo_repost():
            return self.get_c_photo_repost()
        elif self.is_photo_album_repost():
            return 'Пользователь поделился фотоальбомом!'
        elif self.is_good_repost():
            return self.get_c_good_repost()
        elif self.is_music_repost():
            return "Пользователь поделился music!"
        elif self.is_music_list_repost():
            return "Пользователь поделился плейлистом!"
        elif self.is_video_repost():
            return self.get_c_video_repost()
        elif self.is_video_list_repost():
            return "Пользователь поделился видео-альбомом!"
        elif self.is_user_repost():
            return "Пользователь поделился пользователем!"
        elif self.is_community_repost():
            return "Пользователь поделился сообществом!"
        else:
            return False

    def get_u_attach_parent(self):
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
        elif parent.is_user_repost():
            return "u_posts/user_repost.html"
        elif parent.is_community_repost():
            return "u_posts/community_repost.html"
        else:
            return "generic/attach/parent_user.html"

    def get_c_attach_parent(self):
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
        elif parent.is_user_repost():
            return "c_posts/user_repost.html"
        elif parent.is_community_repost():
            return "c_posts/community_repost.html"
        else:
            return "generic/attach/parent_community.html"


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
