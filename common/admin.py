from django.contrib import admin
from common.models import *


class EmojiGroupEmoji(admin.TabularInline):
    model = Emoji


class EmojiGroupAdmin(admin.ModelAdmin):
    inlines = [
        EmojiGroupEmoji
    ]

    list_display = (
        'id',
        'keyword',
        'created',
        'order'
    )


admin.site.register(EmojiGroup, EmojiGroupAdmin)


class EmojiAdmin(admin.ModelAdmin):
    pass


admin.site.register(Emoji, EmojiAdmin)


class ProxyBlacklistDomainAdmin(admin.ModelAdmin):
    list_display = (
        'domain',
    )


admin.site.register(ProxyBlacklistedDomain, ProxyBlacklistDomainAdmin)
