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
        PostCircleInline
    ]

    list_display = (
        'id',
        'created',
        'count_comments',
        'count_reactions',
        'has_text',
        'has_image'
    )


admin.site.register(Post, PostAdmin)
