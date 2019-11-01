from django.contrib import admin

from main.models import *




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
