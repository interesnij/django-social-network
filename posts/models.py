import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone
from pilkit.processors import ResizeToFit
from moderation.models import ModeratedObject
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.models.notification import Notification, notification_handler
from main.models import LikeDislike



class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    content_hard = RichTextUploadingField(blank=True, null=True, config_name='default',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )],
                                      )
    content_lite = RichTextUploadingField(blank=True,null=True,
                                      config_name='lite',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )],
                                      )
    content_medium = RichTextUploadingField(blank=True,
                                      config_name='medium',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )],
                                      )
    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_creator',verbose_name="Создатель")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    #community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='posts',null=True,blank=True,verbose_name="Сообщество")
    is_edited = models.BooleanField(default=False,verbose_name="Изменено")
    is_closed = models.BooleanField(default=False,verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    views=models.IntegerField(default=0,verbose_name="Просмотры")
    votes = GenericRelation(LikeDislike, related_query_name='posts')
    comments = GenericRelation("postcomment")
    reposts = GenericRelation("repost")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "additional_post",
                "actor_name": self.creator.get_full_name()

            }
        async_to_sync(channel_layer.group_send)('notifications', payload)

    def notification_like(self, user):
        notification_handler(user, self.creator,Notification.LIKED, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_dislike(self, user):
        notification_handler(user, self.creator,Notification.DISLIKED, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_comment(self, user):
        notification_handler(user, self.creator,Notification.POST_COMMENT, action_object=self,id_value=str(self.uuid),key='notification')

    def count_likers(self):
        return self.votes.likes().count()

    def count_dislikers(self):
        return self.votes.dislikes().count()

    def get_likers(self):
        return self.votes.likes.all()

    def get_dislikers(self):
        return self.votes.dislikes.all()

    class Meta:
        ordering=["-created"]
        verbose_name="пост"
        verbose_name_plural="посты"

    def __str__(self):
        return self.creator.get_full_name()


class PostComment(models.Model):
    moderated_object = GenericRelation(ModeratedObject, related_query_name='post_comments',verbose_name="Модерация")
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_comments',verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    votes = GenericRelation(LikeDislike, related_query_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def count_replies(self):
        return self.replies.count()

    def update_comment(self, text):
        self.text = text
        self.is_edited = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        self.modified = timezone.now()
        return super(PostComment, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])


class Repost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def get_object_for_content_type(self):
        ct = self.content_type
        model = ct.model_class()
        pk = self.object_id
        object = model.objects.get(pk=pk)
        return object


class PostMute(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='mutes',verbose_name="Пост")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mutes',verbose_name="Кто заглушил")


class PostCommentMute(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='mutes',verbose_name="Пост")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mutes',verbose_name="Кто заглушил")


class PostUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mentions',verbose_name="Упоминаемый")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Пост")


class PostCommentUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mentions',verbose_name="Упомянутый в комментарии")
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Пост")
