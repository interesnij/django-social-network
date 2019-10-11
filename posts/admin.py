from django.contrib import admin

from posts.models import Post, PostComment2


class PostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['is_deleted', 'created',]

class PostCommentAdmin(admin.ModelAdmin):
    list_filter = ['parent_comment',]


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment2, PostCommentAdmin)
