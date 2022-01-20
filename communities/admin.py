from django.contrib import admin
from communities.models import *
from communities.model.settings import *
from communities.model.list import *


class CommunityNotificationsPostInline(admin.TabularInline):
    model = CommunityNotificationsPost
class CommunityNotificationsPhotoInline(admin.TabularInline):
    model = CommunityNotificationsPhoto
class CommunityNotificationsGoodInline(admin.TabularInline):
    model = CommunityNotificationsGood
class CommunityNotificationsVideoInline(admin.TabularInline):
    model = CommunityNotificationsVideo

class CommunityPrivateInline(admin.TabularInline):
    model = CommunityPrivate2
class CommunityInfoInline(admin.TabularInline):
    model = CommunityInfo


class CommunityCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunitySubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['sudcategory', ]

class CommunityAdmin(admin.ModelAdmin):
    inlines = [
        CommunityNotificationsPostInline,
        CommunityNotificationsPhotoInline,
        CommunityNotificationsGoodInline,
        CommunityNotificationsVideoInline,

        CommunityPrivateInline,
        CommunityInfoInline,
    ]

    search_fields = ('name',)
    list_display = ['name','type', 'category']

class CommunityMembershipAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(CommunitySubCategory, CommunitySubCategoryAdmin)
admin.site.register(CommunityCategory, CommunityCategoryAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMembership, CommunityMembershipAdmin)
admin.site.register(CommunityInfo)

admin.site.register(CommunityPostsListPosition)
