from django.contrib import admin
from communities.models import *
from communities.model.settings import *


class CommunityNotificationsSettingsInline(admin.TabularInline):
    model = CommunityNotificationsSettings

class CommunityPrivatePostInline(admin.TabularInline):
    model = CommunityPrivatePost


class CommunityCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunitySubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunityAdmin(admin.ModelAdmin):
    inlines = [
        CommunityNotificationsSettingsInline,
        CommunityPrivatePostInline,
    ]

    search_fields = ('name',)
    list_display = ['name','type', 'category']

class CommunityMembershipAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(CommunitySubCategory, CommunitySubCategoryAdmin)
admin.site.register(CommunityCategory, CommunityCategoryAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMembership, CommunityMembershipAdmin)
