from django.db import models
from django.utils import timezone
from pilkit.processors import ResizeToFit, ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.postgres.indexes import BrinIndex
from main.models import Item


class Article(Item):
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name="Заголовок" )
    image = ProcessedImageField(verbose_name='Главное изображение', blank=False, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, 1024)],
                                 upload_to='articles/%Y/%m/%d')
    content = RichTextUploadingField(config_name='default',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )],
                                      )


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

    class Meta:
        ordering=["-created"]
        verbose_name="статья"
        verbose_name_plural="статьи"

    def __str__(self):
        return self.creator.get_full_name()
