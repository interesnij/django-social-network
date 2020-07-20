from django.contrib import admin
from communities.models import *
from communities.model.settings import *


class CommunityNotificationsPostInline(admin.TabularInline):
    model = CommunityNotificationsPost

class CommunityPrivatePostInline(admin.TabularInline):
    model = CommunityPrivatePost


class CommunityCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunitySubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunityAdmin(admin.ModelAdmin):
    inlines = [
        CommunityNotificationsPostInline,
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
admin.site.register(CommunityPrivatePost)
