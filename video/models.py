import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from communities.models import Community
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from video.helpers import upload_to_video_directory
from common.model.votes import VideoVotes, VideoCommentVotes


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_tracks_count(self):
        return self.video_category.count()

    def is_video_in_category(self, track_id):
        self.video_category.filter(id=track_id).exists()

    def playlist_too(self):
        queryset = self.video_category.all()
        return queryset[:300]

    class Meta:
        verbose_name="Категория ролика"
        verbose_name_plural="Категории ролика"


class VideoTags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_video_in_tag(self, video_id):
        self.video_tag.filter(id=video_id).exists()

    def get_categories(self):
        from django.db.models import Q

        categories_list = []
        categories = self.video_tag.values('category_id')
        categories_ids = [id['category_id'] for id in categories]
        for category in categories_ids:
            if not category in categories_list:
                categories_list = categories_list + [category,]

        categories_query = Q(id__in=categories_list)
        result = VideoCategory.objects.filter(categories_query)
        return result

    def playlist_too(self):
        queryset = self.track_tag.all()
        return queryset

    def get_tracks_count(self):
        return self.video_tag.count()

    class Meta:
        verbose_name="тег"
        verbose_name_plural="теги"


class VideoAlbum(models.Model):
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=250, verbose_name="Название")
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    order = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_creator', verbose_name="Создатель")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False )
    is_generic = models.BooleanField(verbose_name="Сгенерированный", default=False )

    class Meta:
        verbose_name = 'Видеоальбом'
        verbose_name_plural = 'Видеоальбомы'
        ordering = ['order']

    def __str__(self):
        return self.title

    def count_video(self):
        return self.video_album.filter(is_deleted=False).count()

    def get_queryset(self):
        queryset = self.video_album.all().order_by("-created")
        return queryset

    def get_my_queryset(self):
        queryset = self.video_album.filter(is_public=True).order_by("-created")
        return queryset

    def get_video_count(self):
        count = self.video_album.filter(is_public=True).values("pk").count()
        return count

    def get_my_video_count(self):
        count = self.video_album.all().values("pk").count()
        return count


class Video(models.Model):
    image = ProcessedImageField(format='JPEG',
                                options={'quality': 90},
                                upload_to=upload_to_video_directory,
                                processors=[ResizeToFit(width=500, upscale=False)],
                                verbose_name="Обложка")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name="Описание")
    category = models.ForeignKey(VideoCategory, blank=True, null=True, related_name='video_category', on_delete=models.CASCADE, verbose_name="Категория")
    tag = models.ForeignKey(VideoTags, blank=True, null=True, related_name='video_tag', on_delete=models.CASCADE, verbose_name="Тег")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    uri = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ссылка на видео")
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")
    is_child = models.BooleanField(default=True, verbose_name="Доступен детям")
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    album = models.ManyToManyField(VideoAlbum, related_name="video_album", blank=True, verbose_name="Альбом")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Создатель")

    class Meta:
        verbose_name="Видео-ролики"
        verbose_name_plural="Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)

    def likes(self):
        likes = VideoVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = VideoVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = VideoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = VideoVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes[0:6]


class VideoComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name="комментарий к ролику"
        verbose_name_plural="комментарии к ролику"

    def all_visits_count(self):
        from stst.models import VideoNumbers

        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_replies(self):
        get_comments = VideoComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.count()

    def likes(self):
        likes = VideoCommentVotes.objects.filter(photo=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = VideoCommentVotes.objects.filter(photo=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = VideoCommentVotes.objects.filter(photo=self, vote__lt=0)
        return dislikes

    def window_dislikes(self):
        dislikes = VideoCommentVotes.objects.filter(photo=self, vote__lt=0)
        return dislikes[0:6]

    def __str__(self):
        return str(self.item)

    @classmethod
    def create_comment(cls, commenter, video=None, parent_comment=None, text=None, created=None ):
        comment = VideoComment.objects.create(commenter=commenter, parent_comment=parent_comment, video=video, text=text)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "comment_photo",
                "actor_name": comment.commenter.get_full_name()
            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        comment.save()
        return comment
