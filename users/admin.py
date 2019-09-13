from django.contrib import admin

from users.models import User, UserProfile


class UserAdmin(admin.ModelAdmin):
    search_fields = ('last_name',)
    list_filter = ['email']

    class Meta:
            model = User


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['user'] #все поля field.name in Blog._meta.fields
    #fields = []
    #exclude = []
    #list_filter = ['posted']
    search_fields = ['user']
    class Meta:
            model = UserProfile


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
