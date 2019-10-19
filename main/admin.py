from django.contrib import admin

from main.models import Emoji, EmojiGroup, ProxyBlacklistedDomain


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
        'color',
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
