from django.contrib import admin
from .models import *


class SoundParsingAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    class Meta:
            model = SoundParsing


admin.site.register(SoundParsing, SoundParsingAdmin)
admin.site.register(SounGenres)
admin.site.register(SoundList)
admin.site.register(SoundSymbol)
admin.site.register(SoundTags)
