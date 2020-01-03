from django.contrib import admin
from .models import SoundParsing, SounGenres


class SoundParsingAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    class Meta:
            model = SoundParsing


admin.site.register(SoundParsing, SoundParsingAdmin)
admin.site.register(SounGenres)
