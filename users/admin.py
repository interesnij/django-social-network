from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('last_name',)
    list_filter = ['all']

    class Meta:
            model = User


admin.site.register(User, UserAdmin)
