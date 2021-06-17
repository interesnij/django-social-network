from django.contrib import admin
from users.models import User
from users.model.profile import *
from users.model.settings import *
from users.model.list import *

class UserNotificationsInline(admin.TabularInline):
    model = UserNotifications
class UserNotificationsPostInline(admin.TabularInline):
    model = UserNotificationsPost
class UserNotificationsPhotoInline(admin.TabularInline):
    model = UserNotificationsPhoto
class UserNotificationsGoodInline(admin.TabularInline):
    model = UserNotificationsGood
class UserNotificationsVideoInline(admin.TabularInline):
    model = UserNotificationsVideo
class UserNotificationsMusicInline(admin.TabularInline):
    model = UserNotificationsMusic

class UserPrivateInline(admin.TabularInline):
    model = UserPrivate
class UserPrivatePostInline(admin.TabularInline):
    model = UserPrivatePost
class UserPrivatePhotoInline(admin.TabularInline):
    model = UserPrivatePhoto
class UserPrivateGoodInline(admin.TabularInline):
    model = UserPrivateGood
class UserPrivateVideoInline(admin.TabularInline):
    model = UserPrivateVideo
class UserPrivateMusicInline(admin.TabularInline):
    model = UserPrivateMusic

class UserColorSettingsInline(admin.TabularInline):
    model = UserColorSettings

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']
    inlines = [
        UserNotificationsInline,
        UserNotificationsPostInline,
        UserNotificationsPhotoInline,
        UserNotificationsGoodInline,
        UserNotificationsVideoInline,
        UserNotificationsMusicInline,

        UserPrivateInline,
        UserPrivatePostInline,
        UserPrivatePhotoInline,
        UserPrivateGoodInline,
        UserPrivateVideoInline,
        UserPrivateMusicInline,

        UserColorSettingsInline,
    ]
    search_fields = ('last_name','first_name')

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    search_fields = ('name',)

admin.site.register(User, UserAdmin)

admin.site.register(UserBlock)
admin.site.register(UserLocation)
admin.site.register(IPUser)
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(UserFeaturedFriend)
admin.site.register(UserPopulateFriend)
admin.site.register(UserPopulateCommunity)
admin.site.register(UserPostListPosition)
