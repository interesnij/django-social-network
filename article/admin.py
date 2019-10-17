from django.contrib import admin
from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['creator','created', 'is_deleted']
    list_filter = ['is_deleted', 'created',]



admin.site.register(Article, ArticleAdmin)
