from django.contrib import admin

from article.models import Article, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['is_deleted', 'created',]

class ArticleCommentAdmin(admin.ModelAdmin):
    list_filter = ['parent_comment',]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
