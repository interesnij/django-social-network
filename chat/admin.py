from django.contrib import admin
from chat.models import *


class ChatAdmin(admin.ModelAdmin):
    list_display = ("creator", "type")
    list_filter = ("creator", )

class ChatUsersAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "is_administrator")
    list_filter = ("user", )

class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "created", "text", "type", "unread")
    list_filter = ("creator", )


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatUsers, ChatUsersAdmin)
admin.site.register(Message, MessageAdmin)

admin.site.register(MessageVersion)
admin.site.register(MessageOptions) 
