from django.contrib import admin

from connections.models import Connection


class ConnectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    #exclude = ['communities']


admin.site.register(Connection, ConnectionAdmin)
