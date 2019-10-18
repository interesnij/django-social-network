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


class Post(Item):
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=False, null=True, verbose_name="Текст")
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_PUBLISHED = 'P'
    STATUS_ARHIVED = 'A'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликовано'),
        (STATUS_ARHIVED, 'Архивирован'),
    )
    status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_DRAFT, max_length=2, verbose_name="Статус записи")
    image = ProcessedImageField(verbose_name='изображение', blank=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)

    @classmethod
    def create_post(cls, creator, community_name=None, image=None, text=None, video=None,
                    created=None, is_draft=False, good=None, doc=None, question=None):

        post = Post.objects.create(creator=creator, created=created)

        if text:
            post.text = text
        if image:
            post.image = image
        if video:
            post.video = video
        if doc:
            post.doc = doc
        if good:
            post.good = good
        if question:
            post.question = question
        if community_name:
            post.community = Community.objects.get(name=community_name)

        if not is_draft:
            post.publish()
            channel_layer = get_channel_layer()
            payload = {
                    "type": "receive",
                    "key": "additional_post",
                    "actor_name": self.creator.get_full_name()
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

    def _add_media_image(self, image, order):
        return PostImage.create(image=image, post_id=self.pk, order=order)

    def publish(self):
        check_can_be_published(post=self)

        if self.has_media():
            self.status = Post.STATUS_PROCESSING
            self.save()
            process_post_media.delay(post_id=self.pk)
        else:
            self._publish()

    def _publish(self):
        self.status = Post.STATUS_PUBLISHED
        self.created = timezone.now()
        self.save()

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


class PostRepost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_repost', verbose_name="Запись")

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )


class PostMute(models.Model):
    post = models.ForeignKey(Post, db_index=False, on_delete=models.CASCADE, related_name='mutes', verbose_name="Запись")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='post_mutes', verbose_name="Кто заглушил")

    class Meta:
        unique_together = ('post', 'muter',)

    @classmethod
    def create_post_mute(cls, post_id, muter_id):
        return cls.objects.create(post_id=post_id, muter_id=muter_id)



class PostUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='post_mentions', verbose_name="Упоминаемый")
    post = models.ForeignKey(Post, db_index=False, on_delete=models.CASCADE, related_name='user_mentions', verbose_name="Запись")

    class Meta:
        unique_together = ('user', 'post',)



class PostDoc(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_doc', null=True, verbose_name="Документ")
    doc = models.FileField(upload_to=upload_to_post_directory, verbose_name="Документ")
