from django.contrib import admin
from .models import UserProfile


class UserAdmin(admin.ModelAdmin):

    list_display = ['user'] #все поля field.name in Blog._meta.fields
    #fields = []
    #exclude = []
    #list_filter = ['posted']
    search_fields = ['user']
    class Meta:
            model = UserProfile


admin.site.register(UserProfile,UserAdmin)
