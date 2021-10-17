from django.contrib import admin
from docs.models import DocsList, Doc


class DocAdmin(admin.ModelAdmin):
    list_display = ['title','file']
    list_filter = ['created']
    search_fields = ('title',)
    class Meta:
        model = Doc

class DocsListAdmin(admin.ModelAdmin):
    list_display = ['name','community','type','creator']
    search_fields = ('name',)
    class Meta:
        model = DocsList

admin.site.register(Doc, DocAdmin)
admin.site.register(DocsList, DocsListAdmin)
