from django.db import models
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from posts.helpers import upload_to_post_image_directory, upload_to_post_directory
from django.contrib.postgres.indexes import BrinIndex
from main.models import Item
from rest_framework.exceptions import ValidationError


class Post(Item):
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=False, null=True, verbose_name="Текст")


    @classmethod
    def create_post(cls, creator, text=None, community=None, comments_enabled=None, video=None,
                    is_draft=False, good=None, status= None, doc=None, question=None):

        if not text:
            raise ValidationError('Нужно ввести текст или прикрепить фото')
        else:
            post = Post.objects.create(
                                        creator=creator,
                                        text=text,
                                        community=community,
                                        comments_enabled=comments_enabled,
                                        status = status,
                                    )
            channel_layer = get_channel_layer()
            payload = {
                    "type": "receive",
                    "key": "additional_post",
                    "actor_name": post.creator.get_full_name()
                }
            async_to_sync(channel_layer.group_send)('notifications', payload)
        return post

    def is_text_only_post(self):
        return self.has_text() and not self.has_image()

    def has_text(self):
        if hasattr(self, 'text'):
            if self.text:
                return True
        return False

    def has_image(self):
        if hasattr(self, 'image'):
            if self.image:
                return True
        return False

    def get_first_image(self):
        return self.image.first()

    def is_draft(self):
        return self.status == Post.STATUS_DRAFT

    def is_empty(self):
        return not self.text and not hasattr(self, 'image') and not hasattr(self, 'video') and not self.has_media()

    def has_image(self):
        return self.image.exists()

    def delete(self, *args, **kwargs):
        self.delete_image()
        super(Post, self).delete(*args, **kwargs)

    def delete_image(self):
        if self.has_image():
            delete_file_field(self.image.image)

    def soft_delete(self):
        self.delete_notifications()
        for comment in self.comments.all().iterator():
            comment.soft_delete()
        self.is_deleted = True
        self.save()

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
    doc = models.FileField(upload_to=upload_to_post_directory, verbose_name="Документ")
