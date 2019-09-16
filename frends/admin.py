from django.contrib import admin

from frends.models import Connect


class ConnectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    #exclude = ['communities']


admin.site.register(Connection, ConnectionAdmin)
