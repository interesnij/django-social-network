from django.contrib import admin
from posts.models import Post, PostComment


class PostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['is_deleted', 'created',]


class PostCommentAdmin(admin.ModelAdmin):
    search_fields = ('commenter',)
    list_display = ['commenter','created', 'is_deleted']
    list_filter = ['is_deleted']


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
