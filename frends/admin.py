from django.contrib import admin

from frends.models import Connect, ConnectPerm


class ConnectAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ['user','target_user','visited']


admin.site.register(Connect, ConnectAdmin)
admin.site.register(ConnectPerm)
