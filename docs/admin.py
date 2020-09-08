from django.contrib import admin
from docs.models import DocList, Doc


class BlankAdmin(admin.ModelAdmin):
    list_display = ['title','file']
    list_filter = ['created']
    search_fields = ('title',)
    class Meta:
        model = Doc

admin.site.register(Blank, BlankAdmin)
admin.site.register(DocList)
