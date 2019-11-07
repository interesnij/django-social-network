from django.contrib import admin
from notifications.models import Notification, CommunityNotification



admin.site.register(Notification, CommunityNotification)
