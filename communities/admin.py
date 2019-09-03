from django.contrib import admin

from communities.models import Community


class CommunityAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Community, CommunityAdmin)
