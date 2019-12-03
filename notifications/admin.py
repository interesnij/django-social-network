from django.contrib import admin
from notifications.model.user import Notification, CommunityNotification
from notifications.model.item import ItemNotification, ItemCommunityNotification
from notifications.model.photo import PhotoNotification, PhotoCommunityNotification
from notifications.model.good import GoodNotification, GoodCommunityNotification


admin.site.register(Notification)
admin.site.register(CommunityNotification)
admin.site.register(ItemNotification)
admin.site.register(ItemCommunityNotification)
admin.site.register(PhotoNotification)
admin.site.register(GoodCommunityNotification)
admin.site.register(GoodNotification)
admin.site.register(GoodCommunityNotification)
