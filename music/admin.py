from django.contrib import admin
from .models import *


class SoundcloudParsingAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['tag', 'genre']
    class Meta:
            model = SoundcloudParsing

class SoundTagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']
    search_fields = ['name']
    list_filter = ['symbol']
    class Meta:
            model = SoundTags


admin.site.register(SoundcloudParsing, SoundcloudParsingAdmin)
admin.site.register(SoundGenres)
admin.site.register(SoundList)
admin.site.register(SoundSymbol)
admin.site.register(SoundTags, SoundTagsAdmin)
admin.site.register(UserTempSoundList)
