from django.db import models
from pilkit.processors import ResizeToFit, ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from main.models import Item


class Article(Item):
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name="Заголовок" )
    g_image = ProcessedImageField(verbose_name='Главное изображение', blank=False, format='JPEG',options={'quality': 80}, processors=[ResizeToFill(1024, 700)],upload_to='articles/%Y/%m/%d')
    content = RichTextUploadingField(config_name='default',external_plugin_resources=[('youtube','/static/ckeditor_plugins/youtube/youtube/','plugin.js',)],)
    item = models.ManyToManyField("main.Item", blank=True, related_name='item_good')
	item_comment = models.ManyToManyField("main.ItemComment", blank=True, related_name='comment_good')

    @classmethod
    def create_article(cls, creator, title=None, community=None, g_image=None, content=None, created=None, is_draft=False, status= None, comments_enabled=None ):
        article = Article.objects.create(creator=creator,content=content,g_image=g_image,community=community,comments_enabled=comments_enabled,title=title)

        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "additional_post",
                "actor_name": article.creator.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return article


    class Meta:
        ordering=["-created"]
        verbose_name="статья"
        verbose_name_plural="статьи"

    def __str__(self):
        return self.title
