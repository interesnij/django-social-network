from django.contrib import admin

from users.models import Users


class UsersAdmin(admin.ModelAdmin):
    search_fields = ('last_name',)
    #exclude = ['communities']


admin.site.register(Users, UsersAdmin)
