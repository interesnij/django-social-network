from django.contrib import admin

from main.models import *


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


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'creator',
        'created',
        'post',
        'article',
    )

class ItemCommentAdmin(admin.ModelAdmin):
    list_display = (
        'commenter',
        'created',
        'text',
        'parent_comment',
    )

class ItemReactionAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'reactor',
        'emoji',
        'created',
    )

admin.site.register(Item,ItemAdmin)
admin.site.register(ItemComment,ItemCommentAdmin)
admin.site.register(ItemReaction,ItemReactionAdmin)
