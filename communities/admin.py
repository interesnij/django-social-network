from django.contrib import admin
from communities.models import *
from communities.model.settings import *


class CommunityNotificationsPostInline(admin.TabularInline):
    model = CommunityNotificationsPost
class CommunityNotificationsPhotoInline(admin.TabularInline):
    model = CommunityNotificationsPhoto
class CommunityNotificationsGoodInline(admin.TabularInline):
    model = CommunityNotificationsGood
class CommunityNotificationsVideoInline(admin.TabularInline):
    model = CommunityNotificationsVideo

class CommunityPrivatePostInline(admin.TabularInline):
    model = CommunityPrivatePost
class CommunityPrivatePhotoInline(admin.TabularInline):
    model = CommunityPrivatePhoto
class CommunityPrivateGoodInline(admin.TabularInline):
    model = CommunityPrivateGood
class CommunityPrivateVideoInline(admin.TabularInline):
    model = CommunityPrivateVideo

class CommunitySectionsOpenInline(admin.TabularInline):
    model = CommunitySectionsOpen


class CommunityCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunitySubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunityAdmin(admin.ModelAdmin):
    inlines = [
        CommunityNotificationsPostInline,
        CommunityNotificationsPhotoInline,
        CommunityNotificationsGoodInline,
        CommunityNotificationsVideoInline,

        CommunityPrivatePostInline,
        CommunityPrivatePhotoInline,
        CommunityPrivateGoodInline,
        CommunityPrivateVideoInline,

        CommunitySectionsOpenInline,
    ]

    search_fields = ('name',)
    list_display = ['name','type', 'category']

class CommunityMembershipAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(CommunitySubCategory, CommunitySubCategoryAdmin)
admin.site.register(CommunityCategory, CommunityCategoryAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMembership, CommunityMembershipAdmin)
