from django.contrib import admin
from guestbook.models import Guestbook

class GuestAdmin(admin.ModelAdmin):

    list_display = ['user','posted','content'] #все поля field.name in Blog._meta.fields
    #fields = []
    #exclude = []
    list_filter = ['user']
    search_fields = ['user','posted']
    class Meta:
            model = Guestbook

admin.site.register(Guestbook,GuestAdmin)
