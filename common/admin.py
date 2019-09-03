from django.contrib import admin

from common.models import Emoji, EmojiGroup, Badge


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


class BadgeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Badge, BadgeAdmin)
