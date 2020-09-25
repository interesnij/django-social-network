from django.contrib import admin
from chat.models import *


class ChatAdmin(admin.ModelAdmin):
    list_display = ("creator", "type", "is_deleted")
    list_filter = ("creator", )

class ChatUsersAdmin(admin.ModelAdmin):
    list_display = ("user", "chat", "is_administrator")
    list_filter = ("user", )

class MessageAdmin(admin.ModelAdmin):
    list_display = ("creator", "created")
    list_filter = ("creator", )


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatUsers, ChatUsersAdmin)
admin.site.register(Message, MessageAdmin)
