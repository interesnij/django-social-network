from django.contrib import admin
from docs.models import DocList, Doc2


class DocAdmin(admin.ModelAdmin):
    list_display = ['title','file']
    list_filter = ['created']
    search_fields = ('title',)
    class Meta:
        model = Doc2

class DocListAdmin(admin.ModelAdmin):
    list_display = ['name','creator','community']
    list_filter = ['created']
    search_fields = ('title',)
    class Meta:
        model = DocList

admin.site.register(Doc2, DocAdmin)
admin.site.register(DocList, DocListAdmin)
