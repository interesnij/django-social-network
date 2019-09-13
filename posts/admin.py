from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    #exclude = ['communities']


admin.site.register(Post, PostAdmin)
