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


class PostsListAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['name','community','type','creator']


admin.site.register(Post, PostAdmin)
admin.site.register(PostsList, PostsListAdmin)
admin.site.register(PostCategory)
admin.site.register(PostComment, PostCommentAdmin)
