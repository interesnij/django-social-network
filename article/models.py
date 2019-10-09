import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from pilkit.processors import ResizeToFit
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.models.notification import Notification, notification_handler
from main.models import LikeDislike
from article.helpers import upload_to_article_image_directory



class Article(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='article')
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    image = ProcessedImageField(verbose_name='Главное изображение', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_article_image_directory)
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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_creator',verbose_name="Создатель")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='article',null=True,blank=True,verbose_name="Сообщество")
    is_edited = models.BooleanField(default=False,verbose_name="Изменено")
    is_closed = models.BooleanField(default=False,verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    views=models.IntegerField(default=0,verbose_name="Просмотры")
    votes = GenericRelation(LikeDislike, related_query_name='article')
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликована'),
        (STATUS_ARHIVED, 'Архивирована'),
    )
    status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_DRAFT, max_length=2, verbose_name="Статус статьи")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "additional_post",
                "actor_name": self.creator.get_full_name()

            }
        async_to_sync(channel_layer.group_send)('notifications', payload)

    @classmethod
    def create_article(cls, creator, community_name=None, image=None, content_hard=None,
                    created=None, is_draft=False, content_hard=None, content_medium=None ):

        article = Post.objects.create(creator=creator, created=created)
        if community_name:
            article.community = Community.objects.get(name=community_name)

        if not is_draft:
            article.publish()
            channel_layer = get_channel_layer()
            payload = {
                    "type": "receive",
                    "key": "additional_post",
                    "actor_name": self.creator.get_full_name()
                }
            async_to_sync(channel_layer.group_send)('notifications', payload)
        else:
            article.save()
        return article

    def _publish(self):
        self.status = Article.STATUS_PUBLISHED
        self.created = timezone.now()
        self.save()

    def is_draft(self):
        return self.status == Article.STATUS_DRAFT

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
        verbose_name="статья"
        verbose_name_plural="статьи"

    def __str__(self):
        return self.creator.get_full_name()


class ArticleComment(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='article_comment')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='article_replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_comments',verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    votes = GenericRelation(LikeDislike, related_query_name='article_comments_vote')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')

    def count_replies(self):
        return self.replies.count()

    def update_comment(self, text):
        self.text = text
        self.is_edited = True
        self.save()

    def soft_delete(self):
        self.is_deleted = True
        self.delete_notifications()
        self.save()

    def unsoft_delete(self):
        self.is_deleted = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        self.modified = timezone.now()
        return super(ArticleComment, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])


class ArticleRepost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_repost')


class ArticleMute(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='mutes',verbose_name="Статья")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_mutes',verbose_name="Кто заглушил")

    @classmethod
    def create_article_comment_mute(cls, article_comment_id, muter_id):
        return cls.objects.create(article_comment_id=article_comment_id, muter_id=muter_id)


class ArticleCommentMute(models.Model):
    article_comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='mutes',verbose_name="Статья")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_comment_mutes',verbose_name="Кто заглушил")

    @classmethod
    def create_article_comment_mute(cls, article_comment_id, muter_id):
        return cls.objects.create(article_comment_id=article_comment_id, muter_id=muter_id)


class ArticleUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_mentions',verbose_name="Упоминаемый")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Статья")


class ArticleCommentUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_comment_mentions',verbose_name="Упомянутый в комментарии")
    article_comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Статья")
