from django.contrib import admin
from notify.models import *


class NotifyAdmin(admin.ModelAdmin):
    list_display = ['creator', 'recipient', 'verb', 'type']
    #search_fields = ['title']
    list_filter = ['verb', 'type']
    class Meta:
            model = Notify

class WallAdmin(admin.ModelAdmin):
    list_display = ['creator', 'verb', 'type']
    #search_fields = ['title']
    list_filter = ['verb', 'type']
    class Meta:
            model = Wall


admin.site.register(Notify, NotifyAdmin)
admin.site.register(Wall, WallAdmin)
