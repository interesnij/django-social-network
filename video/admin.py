from django.contrib import admin
from video.models import VideoCategory, VideoList, VideoTags, UserTempVideoList, VideoAlbum, Video, VideoComment



admin.site.register(VideoAlbum)
admin.site.register(VideoCategory)
admin.site.register(VideoList)
admin.site.register(VideoTags)
admin.site.register(UserTempVideoList)
admin.site.register(Video)
admin.site.register(VideoComment)
