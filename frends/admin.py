from django.contrib import admin

from frends.models import Connect


class ConnectAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    #exclude = ['communities']


admin.site.register(Connect, ConnectAdmin)
