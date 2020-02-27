from django.contrib import admin
from users.models import *
from users.model.settings import *


class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserNotificationsSettingsInline(admin.TabularInline):
    model = UserNotificationsSettings

class UserPrivateSettingsInline(admin.TabularInline):
    model = UserPrivateSettings

class UserColorSettingsInline(admin.TabularInline):
    model = UserColorSettings

class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline,
        UserNotificationsSettingsInline,
        UserPrivateSettingsInline,
        UserColorSettingsInline,
    ]
    search_fields = ('last_name','first_name')



admin.site.register(User, UserAdmin)

admin.site.register(UserBlock)
