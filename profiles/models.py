from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from imagekit.models import ProcessedImageField
from profiles.helpers import upload_to_user_cover_directory, upload_to_user_avatar_directory
from common.models import Badge
from pilkit.processors import ResizeToFill, ResizeToFit


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, related_name="profile",
                                verbose_name='Пользователь', on_delete=models.CASCADE)
    last_activity= models.DateTimeField(
        default=timezone.now, blank=True, verbose_name='Activity')
    avatar = ProcessedImageField(blank=True, null=True, format='JPEG',
                                 options={'quality': 90}, processors=[ResizeToFill(500, 500)],
                                 upload_to="user/list",verbose_name="Аватар")
    cover = ProcessedImageField(blank=True, null=True, format='JPEG', options={'quality': 90},
                                upload_to=upload_to_user_cover_directory,
                                processors=[ResizeToFit(width=1024, upscale=False)],verbose_name="Фон")
    bio = models.TextField(max_length=300, blank=True, null=True, verbose_name="Биография")
    url = models.URLField(blank=True, null=True,verbose_name="УРЛ")
    followers_count_visible = models.BooleanField(blank=False, null=False, default=False,verbose_name="Число подписчиков видно")
    badges = models.ManyToManyField(Badge, related_name='users_profiles',verbose_name="Значки")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Местоположение")

    def __str__(self):
        return self.user.last_name
