from django.contrib import admin
from users.models import User
from users.model.profile import *
from users.model.settings import UserItemNotifications, UserPrivate, UserColorSettings
from users.model.list import UserBlock


class UserNotificationsSettingsInline(admin.TabularInline):
    model = UserItemNotifications

class UserPrivateSettingsInline(admin.TabularInline):
    model = UserPrivate

class UserColorSettingsInline(admin.TabularInline):
    model = UserColorSettings

class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserNotificationsSettingsInline,
        UserPrivateSettingsInline,
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

admin.site.register(UserStaff)
admin.site.register(CommunityStaff)
admin.site.register(PostUserStaff)
admin.site.register(GoodUserStaff)
admin.site.register(PhotoUserStaff)
admin.site.register(VideoUserStaff)
admin.site.register(MusicUserStaff)

admin.site.register(CanWorkStaffUser)
admin.site.register(CanWorkStaffCommunity)
admin.site.register(CanWorkStaffPostUser)
admin.site.register(CanWorkStaffGoodUser)
admin.site.register(CanWorkStaffPhotoUser)
admin.site.register(CanWorkStaffVideoUser)
admin.site.register(CanWorkStaffAudioUser)
