from django.contrib import admin
from docs.models import DocList, Doc


class DocAdmin(admin.ModelAdmin):
    list_display = ['title','file']
    list_filter = ['created']
    search_fields = ('title',)
    class Meta:
        model = Doc

class DocListAdmin(admin.ModelAdmin):
    list_display = ['name','community','type','creator', 'order']
    search_fields = ('name',)
    class Meta:
        model = DocList

admin.site.register(Doc, DocAdmin)
admin.site.register(DocList, DocListAdmin)
