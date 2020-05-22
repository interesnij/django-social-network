from django.contrib import admin
from video.models import VideoCategory, VideoTags, VideoAlbum, Video, VideoComment



admin.site.register(VideoAlbum)
admin.site.register(VideoCategory)
admin.site.register(VideoTags)
admin.site.register(Video)
admin.site.register(VideoComment)
