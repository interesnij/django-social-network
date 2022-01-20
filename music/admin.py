from django.contrib import admin
from .models import *


class MusicAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['genre']
    class Meta:
            model = Music


class MusicListAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['name','type','creator', 'community']

admin.site.register(Music, MusicAdmin)
admin.site.register(SoundGenres)
admin.site.register(MusicList, MusicListAdmin)
admin.site.register(UserTempMusicList)
