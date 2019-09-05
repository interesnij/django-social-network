from django.contrib import admin

from connections.models import Connections


class ConnectionsAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    #exclude = ['communities']


admin.site.register(Connections, ConnectionsAdmin)
