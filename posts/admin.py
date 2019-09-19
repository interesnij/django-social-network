from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator', 'created', 'community', 'is_deleted',]
    list_filter = ['community', 'is_deleted', 'created',]


admin.site.register(Post, PostAdmin)
