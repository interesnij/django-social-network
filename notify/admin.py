from django.contrib import admin
from notify.model.user import UserNotify, UserCommunityNotify
from notify.model.item import ItemNotify, ItemCommunityNotify
from notify.model.photo import PhotoNotify, PhotoCommunityNotify
from notify.model.good import GoodNotify, GoodCommunityNotify
from notify.model.video import VideoNotify, VideoCommunityNotify


admin.site.register(UserNotify)
admin.site.register(UserCommunityNotify)
admin.site.register(ItemNotify)
admin.site.register(ItemCommunityNotify)
admin.site.register(PhotoNotify)
admin.site.register(PhotoCommunityNotify)
admin.site.register(GoodNotify)
admin.site.register(GoodCommunityNotify)
admin.site.register(VideoNotify)
admin.site.register(VideoCommunityNotify)
