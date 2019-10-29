from django.contrib import admin

from communities.models import CommunityCategory, CommunitySubCategory, Community, CommunityMembership


class CommunityCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunitySubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunityAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunityMembershipAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(CommunitySubCategory, CommunitySubCategoryAdmin)
admin.site.register(CommunityCategory, CommunityCategoryAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMembership, CommunityMembershipAdmin)
