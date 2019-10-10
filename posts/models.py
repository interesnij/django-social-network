import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from pilkit.processors import ResizeToFill, ResizeToFit
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.models import Notification, notification_handler
from main.models import LikeDislike
from posts.helpers import upload_to_post_image_directory, upload_to_post_directory


class Post(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='post')
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=False, null=True, verbose_name="Текст")
    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_creator', verbose_name="Создатель")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='posts', null=True, blank=True, verbose_name="Сообщество")
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_closed = models.BooleanField(default=False, verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    views=models.IntegerField(default=0, verbose_name="Просмотры")
    votes = GenericRelation(LikeDislike, related_query_name='posts')
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

    @classmethod
    def create_post(cls, creator, community_name=None, image=None, text=None, video=None,
                    created=None, is_draft=False, good=None, doc=None, question=None):

        post = Post.objects.create(creator=creator, created=created)

        if text:
            post.text = text
        if image:
            post.add_media(file=image)
        if video:
            post.add_media(file=video)
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
        verbose_name="Запись"
        verbose_name_plural="Записи"

    def __str__(self):
        return self.creator.get_full_name()


class PostImage(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='image', null=True)
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
    image9 = ProcessedImageField(verbose_name='Изображение 9', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)
    image10 = ProcessedImageField(verbose_name='Изображение 10', blank=False, null=True, format='JPEG',
                                 options={'quality': 80}, processors=[ResizeToFill(1024, upscale=False)],
                                 upload_to=upload_to_post_image_directory)

    @classmethod
    def create_post_image(cls, image, post_id):
        return cls.objects.create(image=image, post_id=post_id)


class PostComment(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='post_comment')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создан")
    modified = models.DateTimeField(db_index=True, default=timezone.now)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_comments', verbose_name="Комментатор")
    text = models.TextField(max_length=settings.POST_COMMENT_MAX_LENGTH, blank=True, null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False, verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False, verbose_name="Удаено")
    votes = GenericRelation(LikeDislike, related_query_name='post_comments_vote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', verbose_name="Запись")

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


class PostRepost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_repost', verbose_name="Запись")


class PostMute(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='mutes', verbose_name="Запись")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mutes', verbose_name="Кто заглушил")

    @classmethod
    def create_post_mute(cls, post_id, muter_id):
        return cls.objects.create(post_id=post_id, muter_id=muter_id)


class PostCommentMute(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='mutes', verbose_name="Запись")
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mutes', verbose_name="Кто заглушил")

    @classmethod
    def create_post_comment_mute(cls, post_comment_id, muter_id):
        return cls.objects.create(post_comment_id=post_comment_id, muter_id=muter_id)


class PostUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mentions', verbose_name="Упоминаемый")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_mentions', verbose_name="Запись")


class PostCommentUserMention(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mentions', verbose_name="Упомянутый в комментарии")
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='user_mentions', verbose_name="Запись")


class PostDoc(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_doc', null=True, verbose_name="Документ")
    doc = models.FileField(upload_to=upload_to_post_directory, verbose_name="Документ")
