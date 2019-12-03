from django.contrib import admin
from notifications.model.user import UserNotification, UserCommunityNotification
from notifications.model.item import ItemNotification, ItemCommunityNotification
from notifications.model.photo import PhotoNotification, PhotoCommunityNotification
from notifications.model.good import GoodNotification, GoodCommunityNotification


admin.site.register(UserNotification)
admin.site.register(UserCommunityNotification)
admin.site.register(ItemNotification)
admin.site.register(ItemCommunityNotification)
admin.site.register(PhotoNotification)
admin.site.register(PhotoCommunityNotification)
admin.site.register(GoodNotification)
admin.site.register(GoodCommunityNotification)
