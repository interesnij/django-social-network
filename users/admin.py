from django.contrib import admin
from users.models import User, UserProfile, UserNotificationsSettings, UserPrivateSettings


class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserNotificationsSettingsInline(admin.TabularInline):
    model = UserNotificationsSettings


class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline,
        UserNotificationsSettingsInline,
        UserPrivateSettings,
    ]
    search_fields = ('last_name',)



admin.site.register(User, UserAdmin)
