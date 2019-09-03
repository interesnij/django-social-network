from django.contrib import admin

from users.models import User


class UsersAdmin(admin.ModelAdmin):
    search_fields = ('last_name',)
    #exclude = ['communities']


admin.site.register(User, UserAdmin)
