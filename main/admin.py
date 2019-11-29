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

admin.site.register(Item,ItemAdmin)
admin.site.register(ItemComment,ItemCommentAdmin)
