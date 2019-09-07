from django.contrib import admin
from a_category.models import ACategory

class ACategoryAdmin(admin.ModelAdmin):

    list_display = ['name','order'] #все поля field.name in Blog._meta.fields
    #fields = []
    #exclude = []
    #list_filter = ['posted']
    search_fields = ['name']
    class Meta:
            model = ACategory

admin.site.register(ACategory,ACategoryAdmin)
