from django.contrib import admin
from video.models import VideoCategory, VideoAlbum, Video, VideoComment



admin.site.register(VideoAlbum)
admin.site.register(VideoCategory)
admin.site.register(Video)
admin.site.register(VideoComment)
