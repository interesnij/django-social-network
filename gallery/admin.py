from django.contrib import admin
from gallery.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['creator', ]

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['creator', ]

admin.site.register(Album)
admin.site.register(Photo)
