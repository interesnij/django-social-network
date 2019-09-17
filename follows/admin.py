from django.contrib import admin
from follows.models import Follow


class FollowAdmin(admin.ModelAdmin):
    search_fields = ('user',)


admin.site.register(Follow, FollowAdmin)
