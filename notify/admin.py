from django.contrib import admin
from notify.model.user import UserNotify, UserCommunityNotify
from notify.model.post import PostNotify, PostCommunityNotify
from notify.model.photo import PhotoNotify, PhotoCommunityNotify
from notify.model.good import GoodNotify, GoodCommunityNotify
from notify.model.video import VideoNotify, VideoCommunityNotify


admin.site.register(UserNotify)
admin.site.register(UserCommunityNotify)
admin.site.register(PostNotify)
admin.site.register(PostCommunityNotify)
admin.site.register(PhotoNotify)
admin.site.register(PhotoCommunityNotify)
admin.site.register(GoodNotify)
admin.site.register(GoodCommunityNotify)
admin.site.register(VideoNotify)
admin.site.register(VideoCommunityNotify)
