from django.contrib import admin
from common.models import *


class ProxyBlacklistDomainAdmin(admin.ModelAdmin):
    list_display = (
        'domain',
    )

class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = (
        'vote',
        'user',
        'parent',
    )


admin.site.register(ProxyBlacklistedDomain, ProxyBlacklistDomainAdmin)
admin.site.register(LikeDislike, LikeDislikeAdmin)
