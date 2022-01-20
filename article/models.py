from django.db import models
import uuid
from pilkit.processors import ResizeToFit, ResizeToFill
from django.conf import settings
from imagekit.models import ProcessedImageField
from django.contrib.postgres.indexes import BrinIndex
from django.db.models import Q


class Article(models.Model):
    PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = 'PUB','PRI','MAN','_DEL','_CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name="Заголовок" )
    g_image = ProcessedImageField(verbose_name='Главное изображение', blank=False, format='JPEG',options={'quality': 80}, processors=[ResizeToFill(1024, 700)],upload_to='articles/%Y/%m/%d')
    #content = RichTextUploadingField(config_name='default',external_plugin_resources=[('youtube','/static/ckeditor_plugins/youtube/youtube/','plugin.js',)],)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    #community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='article_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(choices=TYPE, max_length=5, verbose_name="Статус статьи")

    #users = models.ManyToManyField("users.User", blank=True, related_name='users_article')
    #communities = models.ManyToManyField('communities.Community', blank=True, related_name='communities_article')

    @classmethod
    def create_article(cls, creator, title, community, g_image, content, created ):
        article = Article.objects.create(creator=creator,content=content,g_image=g_image,community=community,title=title)

        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "additional_post",
                "actor_name": article.creator.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return article

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    class Meta:
        ordering = ["-created"]
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.title
