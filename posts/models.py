from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from main.models import Item
from rest_framework.exceptions import ValidationError


class Post(Item):
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=False, null=True, verbose_name="Текст")

    @classmethod
    def create_post(cls, creator, text=None, community=None, comments_enabled=None, is_draft=False, status= None):
        post = Post.objects.create(creator=creator, text=text, community=community, comments_enabled=comments_enabled, status = status, )
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "additional_post",
            "actor_name": post.creator.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
    return post

    class Meta:
        ordering=["-created"]
        verbose_name="Запись"
        verbose_name_plural="Записи"

    def __str__(self):
        return self.creator.get_full_name()


class PostUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='post_mentions', verbose_name="Упоминаемый")
    post = models.ForeignKey(Post, db_index=False, on_delete=models.CASCADE, related_name='user_mentions', verbose_name="Запись")


class PostDoc(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_doc', null=True, verbose_name="Документ")
    doc = models.FileField(upload_to="posts/", verbose_name="Документ")
