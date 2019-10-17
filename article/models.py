from django.db import models
from django.utils import timezone
from pilkit.processors import ResizeToFit, ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.models import Notification, notification_handler
from django.contrib.postgres.indexes import BrinIndex
from main.models import Item


class Article(Item):
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name="Заголовок" )
    image = ProcessedImageField(verbose_name='Главное изображение', blank=False, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, 650)],
                                 upload_to='articles/%Y/%m/%d')
    content = RichTextUploadingField(config_name='default',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )],
                                      )
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
    status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_DRAFT, max_length=2, verbose_name="Статус статьи")


    @classmethod
    def create_article(cls, creator, community_name=None, image=None, content_hard=None,
                    created=None, is_draft=False, content_lite=None, content_medium=None ):

        article = Article.objects.create(creator=creator, created=created)
        if community_name:
            article.community = Community.objects.get(name=community_name)
        if image:
            article.image=image
        if content:
            article.content_medium=content_medium

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

    def count_comments(self):
        parent_comments = ArticleComment.objects.filter(article=self).count()
        return parent_comments

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


class ArticleRepost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_repost')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )


class ArticleMute(models.Model):
    article = models.ForeignKey(Article, db_index=False, on_delete=models.CASCADE, related_name='mutes',verbose_name="Статья")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='article_mutes',verbose_name="Кто заглушил")

    @classmethod
    def create_article_comment_mute(cls, article_comment_id, muter_id):
        return cls.objects.create(article_comment_id=article_comment_id, muter_id=muter_id)

    class Meta:
        unique_together = ('article', 'muter',)


class ArticleUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='article_mentions',verbose_name="Упоминаемый")
    article = models.ForeignKey(Article, db_index=False, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Статья")

    class Meta:
        unique_together = ('user', 'article',)
