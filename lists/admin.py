from django.contrib import admin
from lists.models import *


class AuthorityListAdmin(admin.ModelAdmin):
    list_display = ['name','slug','category','order']
    search_fields = ('name',)
    class Meta:
        model = AuthorityList

class ElectNewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    search_fields = ('name',)
    class Meta:
        model = ElectNewsCategory

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    search_fields = ('name',)
    class Meta:
        model = BlogCategory

class FractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    search_fields = ('name',)
    class Meta:
        model = Fraction

admin.site.register(AuthorityList, AuthorityListAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(ElectNewsCategory)
admin.site.register(AuthorityListCategory)
admin.site.register(Fraction, FractionAdmin)
