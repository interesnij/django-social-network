from django.contrib import admin
from notify.models import Notify


class NotifyAdmin(admin.ModelAdmin):
    list_display = ['creator','recipient','created']
    list_filter = ['created']
    class Meta:
        model = Notify


admin.site.register(Notify, NotifyAdmin)
