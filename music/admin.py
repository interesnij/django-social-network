from django.contrib import admin
from .models import *


class MusicAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['tag', 'genre']
    class Meta:
            model = Music

class SoundTagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']
    search_fields = ['name']
    list_filter = ['symbol']
    class Meta:
            model = SoundTags


class MusicListAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['name','community','type','creator']

admin.site.register(Music, MusicAdmin)
admin.site.register(SoundGenres)
admin.site.register(MusicList, MusicListAdmin)
admin.site.register(SoundSymbol)
admin.site.register(SoundTags, SoundTagsAdmin)
admin.site.register(UserTempMusicList)
