from django.contrib import admin

from communities.models import Community,CommunityMembership


class CommunityAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CommunityMembershipAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMembership, CommunityMembershipAdmin)
