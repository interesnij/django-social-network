from django.contrib import admin

from posts.models import Post, PostComment


class PostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator', 'created', 'community', 'is_deleted',]
    list_filter = ['community', 'is_deleted', 'created',]

class PostCommentAdmin(admin.ModelAdmin):
    list_filter = ['parent_comment', 'commenter',]


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
