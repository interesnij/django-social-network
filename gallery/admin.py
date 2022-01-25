from django.contrib import admin
from gallery.models import PhotoList, Photo, PhotoComment


class PhotoListAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'type', 'created', 'community']
    list_filter = ['creator', ]
    class Meta:
        model = PhotoList

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['creator', 'created']
    list_filter = ['creator', ]

    class Meta:
            model = Photo

admin.site.register(PhotoList, PhotoListAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoComment)
