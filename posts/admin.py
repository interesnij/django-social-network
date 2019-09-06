from django.contrib import admin
from circles.models import Circle
from posts.models import Post, PostComment



class PostAdmin(admin.ModelAdmin):


    list_display = (
        'creator',
        'created',
        'community',
    )


admin.site.register(Post, PostAdmin)
