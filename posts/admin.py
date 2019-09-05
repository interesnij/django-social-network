from django.contrib import admin
from circles.models import Circle
from posts.models import Post, PostImage, PostComment, PostReaction


class PostImageInline(admin.TabularInline):
    model = PostImage


class PostCommentInline(admin.TabularInline):
    model = PostComment

    readonly_fields = (
        'text',
        'created'
    )


class PostReactionInline(admin.TabularInline):
    model = PostReaction

    readonly_fields = [
        'emoji'
    ]


class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostReactionInline,
        PostImageInline,
        PostCommentInline,
    ]

    list_display = (
        'creator',
        'created',
        'community',
    )


admin.site.register(Post, PostAdmin)
