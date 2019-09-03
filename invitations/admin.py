from django.contrib import admin
from invitations.models import UserInvite



class UserInviteAdmin(admin.ModelAdmin):
    model = UserInvite
    search_fields = ('email')
    list_display = ('name', 'email',) #'created_user', 'badge'
    list_display_links = ['email']


admin.site.register(UserInvite, UserInviteAdmin)
