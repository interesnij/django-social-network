from django.contrib import admin
from posts.models import *


class PostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = [
                    'creator',
                    #'community',
                    'created',
                    ]
    list_filter = ['created',]


class PostCommentAdmin(admin.ModelAdmin):
    search_fields = ('commenter',)
    list_display = ['commenter','created']


class PostListAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['name','community','type','creator', 'order']


admin.site.register(Post, PostAdmin)
admin.site.register(PostList, PostListAdmin)
admin.site.register(PostCategory)
admin.site.register(PostComment, PostCommentAdmin)
