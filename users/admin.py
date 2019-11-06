from django.contrib import admin
from users.models import User, UserProfile, UserNotificationsSettings, UserPrivateSettings


class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserNotificationsSettingsInline(admin.TabularInline):
    model = UserNotificationsSettings

class UserPrivateSettingsInline(admin.TabularInline):
    model = UserPrivateSettings


class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline,
        UserNotificationsSettingsInline,
        UserPrivateSettingsInline,
    ]
    search_fields = ('last_name',)



admin.site.register(User, UserAdmin)
