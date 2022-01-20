from django.contrib import admin
from video.models import VideoCategory, VideoList, Video, VideoComment



class VideoListAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['name','type','creator',]

admin.site.register(VideoList, VideoListAdmin)
admin.site.register(VideoCategory)
admin.site.register(Video)
admin.site.register(VideoComment)
