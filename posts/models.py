import uuid
from datetime import timedelta
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count
from pilkit.processors import ResizeToFit
from rest_framework.exceptions import ValidationError
#from moderation.models import ModeratedObject

from django.conf import settings
from common.models import Emoji
#from common.utils.helpers import delete_file_field, sha256sum, extract_usernames_from_string

from imagekit.models import ProcessedImageField
#from notifications.helpers import send_post_comment_user_mention_push_notification, \
    #send_post_user_mention_push_notification
from posts.helpers import upload_to_post_image_directory, upload_to_post_video_directory


class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True,verbose_name="uuid")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=False, null=True,verbose_name="Текст")
    created = models.DateTimeField(editable=False, db_index=True,verbose_name="Создан")
    #creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts',verbose_name="Создатель")
    comments_enabled = models.BooleanField(default=True, editable=False, null=False,verbose_name="Разрешить комментарии")
    public_reactions = models.BooleanField(default=True, editable=False, null=False,verbose_name="Публичная реакция")
    #community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='posts',null=True,blank=False,verbose_name="Сообщество")
    is_edited = models.BooleanField(default=False,verbose_name="Изменено")
    is_closed = models.BooleanField(default=False,verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")


class PostImage(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='image',verbose_name="Пост")
    image = ProcessedImageField(verbose_name='изображение',
                                upload_to=upload_to_post_image_directory,
                                width_field='width',
                                height_field='height',
                                blank=False, null=True, format='JPEG', options={'quality': 100},
                                processors=[ResizeToFit(width=1024, upscale=False)])
    width = models.PositiveIntegerField(editable=False, null=False, blank=False,verbose_name="Высота")
    height = models.PositiveIntegerField(editable=False, null=False, blank=False,verbose_name="Ширина")
    hash = models.CharField(max_length=64, blank=False, null=True,verbose_name="Хэш")


class PostVideo(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='video',verbose_name="Пост")
    video = models.FileField(blank=False, null=False,
                             upload_to=upload_to_post_video_directory,
                             verbose_name="Видео")
    hash = models.CharField(max_length=64, blank=False, null=True,verbose_name="Хэш")


class PostComment(models.Model):
    #moderated_object = GenericRelation(ModeratedObject, related_query_name='post_comments',verbose_name="Модерация")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',verbose_name="Пост")
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(editable=False, db_index=True,verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_comments',verbose_name="Комментатор")
    text = models.TextField(max_length=settings.POST_COMMENT_MAX_LENGTH, blank=False, null=False,verbose_name="Текст")
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    # Это происходит только в том случае, если комментарий был сообщен и найден с критическим содержанием серьезности
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    created = models.DateTimeField(editable=False)
    #reactor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_reactions')
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='post_reactions')



class PostCommentReaction(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='reactions',verbose_name="Комментарий к посту")
    created = models.DateTimeField(editable=False,verbose_name="Создан")
    #reactor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_reactions',verbose_name="Кто отреагировал")
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='post_comment_reactions',verbose_name="Смайл")


class PostMute(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='mutes',verbose_name="Пост")
    #muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mutes',verbose_name="Кто заглушил")


class PostCommentMute(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='mutes',verbose_name="Пост")
    #muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mutes',verbose_name="Кто заглушил")


class PostUserMention(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mentions',verbose_name="Упоминаемый")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Пост")


class PostCommentUserMention(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mentions',verbose_name="Упомянутый в комментарии")
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='user_mentions',verbose_name="Пост")
