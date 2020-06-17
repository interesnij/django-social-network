import uuid
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
#from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from notifications.model.photo import *
from gallery.helpers import upload_to_photo_directory
from common.model.votes import PhotoVotes, PhotoCommentVotes


class Album(models.Model):
    #moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='albums')
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    is_generic = models.BooleanField(default=False, verbose_name="Сгенерированный альбом")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_user', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def __str__(self):
        return self.title

    def get_cover_photo_for_avatars(self):
        if self.cover_photo:
            return self.cover_photo
        else:
            return Photo.objects.filter(album=self, is_generic=True, title="Фото со страницы").last()
    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo
        elif Photo.objects.filter(album=self, is_deleted=False).exists():
            photo = Photo.objects.filter(album=self, is_deleted=False).last()
            return photo
        else:
            return False

    def count_photo(self):
        return self.album.filter(is_deleted=False).count()

    def album_is_generic(self):
        if self.is_generic:
            return True
        else:
            return False


class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    #moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='photos')
    album = models.ManyToManyField(Album, related_name="album", blank=True)
    file = ProcessedImageField(format='JPEG', options={'quality': 90}, upload_to=upload_to_photo_directory, processors=[ResizeToFit(width=1024, upscale=False)])
    description = models.TextField(max_length=250, blank=True, null=True, verbose_name="Описание")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False )
    item = models.ManyToManyField('posts.Post', blank=True, related_name='item_photo')
    item_comment = models.ManyToManyField('posts.PostComment', blank=True, related_name='comment_photo')
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-created"]

    @classmethod
    def create_photo(cls, creator, album=None, file=None, community=None, created=None, is_public=None, description=None, item=None ):
        photo = Photo.objects.create(creator=creator, file=file, community=community, is_public=is_public, album=album, description=description, item=item, )
        return photo

    @classmethod
    def create_avatar(cls, creator, album=None, file=None, community=None, created=None, is_public=None, description=None):
        photo = Photo.objects.create(creator=creator, file=file, community=community, is_public=is_public, album=album, description=description,)
        return photo

    def notification_user_repost(self, user):
        photo_notification_handler(user, self.creator, verb=PhotoNotification.REPOST, key='social_update', photo=self, comment=None)

    def notification_user_like(self, user):
        photo_notification_handler(user, self.creator, verb=PhotoNotification.LIKE, key='social_update', photo=self, comment=None)

    def notification_user_dislike(self, user):
        photo_notification_handler(user, self.creator, verb=PhotoNotification.DISLIKE, key='social_update', photo=self, comment=None)

    def notification_community_repost(self, user):
        photo_community_notification_handler(actor=user, recipient=None, verb=PhotoCommunityNotification.REPOST, key='social_update', community=self.community, photo=self, comment=None)

    def notification_community_like(self, user):
        photo_community_notification_handler(actor=user, recipient=None, verb=PhotoCommunityNotification.LIKE, key='social_update', community=self.community, photo=self, comment=None)

    def notification_community_dislike(self, user):
        photo_community_notification_handler(actor=user, recipient=None, verb=PhotoCommunityNotification.DISLIKE, key='social_update', community=self.community, photo=self, comment=None)

    def get_comments(self, user):
        comments_query = self._make_get_comments_for_post_query(user=user)
        return PhotoComment.objects.filter(comments_query)

    def get_comment_replies(self, post_comment_id):
        post_comment = PhotoComment.objects.get(pk=post_comment_id)
        return self.get_comment_replies_for_comment_with_post(post_comment=post_comment)

    def is_avatar(self, user):
        try:
            avatar = user.get_avatar_photos().order_by('-id')[0]
            if avatar == self:
                return True
            else:
                return None
        except:
            return None

    def get_comment_replies_for_comment_with_post(self, post_comment):
        comment_replies_query = self._make_get_comments_for_post_query(self, post_comment_parent_id=post_comment.pk)
        return PostComment.objects.filter(comment_replies_query)

    def _make_get_comments_for_post_query(self, user, post_comment_parent_id=None):
        comments_query = Q(photo_id=self.pk)
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
        likes = PhotoVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = PhotoVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = PhotoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = PhotoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes[0:6]

    def get_reposts(self):
        parents = Photo.objects.filter(parent=self)
        return parents

    def get_window_reposts(self):
        parents = Photo.objects.filter(parent=self)
        return parents[0:6]

    def count_reposts(self):
        parents = self.get_reposts()
        count_reposts = parents.count()
        return count_reposts

    def get_likes_for_item(self, user):
        reactions_query = user._make_get_votes_query(photo=self)
        return PhotoVotes.objects.filter(parent=self, vote__gt=0).filter(reactions_query)

    def get_dislikes_for_item(self, user):
        reactions_query = user._make_get_votes_query(photo=self)
        return PhotoVotes.objects.filter(parent=self, vote__lt=0).filter(reactions_query)


class PhotoComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    #moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='photo_comment')

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def notification_user_comment(self, user):
        item_notification_handler(user, self.commenter, verb=PhotoNotification.POST_COMMENT, comment=self, photo=self.photo, key='social_update')

    def notification_user_reply_comment(self, user):
        item_notification_handler(user, self.commenter, verb=PhotoNotification.POST_COMMENT_REPLY, photo=self.parent_comment.photo, comment=self.parent_comment, key='social_update')

    def notification_user_comment_like(self, user):
        item_notification_handler(actor=user, recipient=None, verb=PhotoNotification.LIKE_COMMENT, photo=self.photo, comment=self, key='social_update')

    def notification_user_comment_dislike(self, user):
        item_notification_handler(actor=user, recipient=None, verb=PhotoNotification.DISLIKE_COMMENT, photo=self.photo, comment=self, key='social_update')

    def notification_community_comment(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.photo.community, photo=self.photo, verb=PhotoCommunityNotification.POST_COMMENT, comment=self, key='social_update')

    def notification_community_reply_comment(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.parent_comment.photo.community, photo=self.parent_comment.photo, verb=PhotoCommunityNotification.POST_COMMENT_REPLY, comment=self.parent_comment, key='social_update')

    def notification_community_comment_like(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.photo.community, verb=PhotoCommunityNotification.LIKE_COMMENT, comment=self, photo=self.photo, key='social_update')

    def notification_community_comment_dislike(self, user):
        item_community_notification_handler(actor=user, recipient=None, community=self.photo.community, verb=PhotoCommunityNotification.DISLIKE_COMMENT, comment=self, photo=self.photo, key='social_update')

    def get_replies(self):
        get_comments = PhotoComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.count()

    def likes(self):
        likes = PhotoCommentVotes.objects.filter(photo=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = PhotoCommentVotes.objects.filter(photo=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = PhotoCommentVotes.objects.filter(photo=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = PhotoCommentVotes.objects.filter(photo=self, vote__lt=0)
        return dislikes[0:6]

    def get_likes_for_comment_item(self, user):
        reactions_query = user._make_get_votes_query_comment(comment=self)
        return PhotoCommentVotes.objects.filter(photo=self, vote__gt=0).filter(reactions_query)

    def get_dislikes_for_comment_item(self, user):
        reactions_query = user._make_get_votes_query_comment(comment=self)
        return PhotoCommentVotes.objects.filter(photo=self, vote__lt=0).filter(reactions_query)

    def __str__(self):
        return str(self.item)

    @classmethod
    def create_comment(cls, commenter, photo=None, parent_comment=None, text=None, created=None ):
        comment = PhotoComment.objects.create(commenter=commenter, parent_comment=parent_comment, photo=photo, text=text)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "comment_photo",
                "actor_name": comment.commenter.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        comment.save()
        return comment
