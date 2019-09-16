from django.contrib import admin
from notifications.models import Notification



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'verb', 'unread', )
    list_filter = ('recipient', 'unread', )
