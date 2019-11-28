from django.contrib import admin
from gallery.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['creator', ]

    class Meta:
            model = Album

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['creator', ]

    class Meta:
            model = Photo

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
