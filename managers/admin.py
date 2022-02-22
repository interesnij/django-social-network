from django.contrib import admin
from managers.models import *


class ModerationReportInline(admin.TabularInline):
    model = ModerationReport

class ModeratedAdmin(admin.ModelAdmin):
    inlines = [
        ModerationReportInline,
    ]
    list_display = ['type', 'object_id', 'description', 'status', 'verified']
    search_fields = ['type']
    class Meta:
            model = Moderated

class ModerationPenaltyAdmin(admin.ModelAdmin):
    list_display = ['type', 'object_id', 'status', 'moderated_object']
    search_fields = ['type']
    class Meta:
            model = ModerationPenalty

class SupportUsersAdmin(admin.ModelAdmin):
    list_display = ['level', 'manager', 'points', 'chats']
    search_fields = ['level']
    class Meta:
            model = SupportUsers


admin.site.register(Moderated, ModeratedAdmin)
admin.site.register(ModerationPenalty, ModerationPenaltyAdmin)
admin.site.register(SupportUsers, SupportUsersAdmin)
