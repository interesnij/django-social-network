from django.contrib import admin
from gallery.models import Album, Photo



admin.site.register(Album, Photo)
