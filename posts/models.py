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
    image = ProcessedImageField(verbose_name='Главное изображение', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image2 = ProcessedImageField(verbose_name='Изображение 2', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image3 = ProcessedImageField(verbose_name='Изображение 3', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image4 = ProcessedImageField(verbose_name='Изображение 4', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image5 = ProcessedImageField(verbose_name='Изображение 5', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image6 = ProcessedImageField(verbose_name='Изображение 6', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image7 = ProcessedImageField(verbose_name='Изображение 7', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image8 = ProcessedImageField(verbose_name='Изображение 8', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)

    @classmethod
    def create_post(cls, creator, text=None, community_name=None, image=None, video=None,
                    is_draft=False, good=None, doc=None, question=None):

        if not text and not image:
            raise ValidationError('Нужно ввести текст или прикрепить фото')
        else:
            post = Post.objects.create(creator=creator, created=created)

        if text:
            post.text = text
        if community_name:
            post.community = Community.objects.get(name=community_name)

        if not is_draft:
            post.STATUS_PUBLISHED
            channel_layer = get_channel_layer()
            payload = {
                    "type": "receive",
                    "key": "additional_post",
                    "actor_name": post.creator.get_full_name()
                }
            async_to_sync(channel_layer.group_send)('notifications', payload)
        else:
            post.save()
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


class PostImage(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='post_image', null=True)
    image = ProcessedImageField(verbose_name='Главное изображение', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image2 = ProcessedImageField(verbose_name='Изображение 2', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image3 = ProcessedImageField(verbose_name='Изображение 3', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image4 = ProcessedImageField(verbose_name='Изображение 4', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image5 = ProcessedImageField(verbose_name='Изображение 5', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image6 = ProcessedImageField(verbose_name='Изображение 6', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image7 = ProcessedImageField(verbose_name='Изображение 7', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image8 = ProcessedImageField(verbose_name='Изображение 8', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)


class PostUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='post_mentions', verbose_name="Упоминаемый")
    post = models.ForeignKey(Post, db_index=False, on_delete=models.CASCADE, related_name='user_mentions', verbose_name="Запись")




class PostDoc(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_doc', null=True, verbose_name="Документ")
    doc = models.FileField(upload_to=upload_to_post_directory, verbose_name="Документ")
