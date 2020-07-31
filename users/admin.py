from django.contrib import admin
from users.models import User
from users.model.profile import *
from users.model.settings import *
from users.model.list import UserBlock


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
    list_display = ['user','b_avatar', 's_avatar']

admin.site.register(User, UserAdmin)

admin.site.register(UserBlock)
admin.site.register(OneUserLocation)
admin.site.register(TwoUserLocation)
admin.site.register(ThreeUserLocation)
admin.site.register(IPUser)
admin.site.register(UserProfile, UserProfileAdmin)
