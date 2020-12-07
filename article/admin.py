from django.contrib import admin
from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator','created',]
    list_filter = ['created',]

admin.site.register(Article, ArticleAdmin)
