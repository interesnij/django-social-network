from django.contrib import admin
from managers.models import *


class ModerationReportInline(admin.TabularInline):
    model = ModerationReport

class ModerationAdmin(admin.ModelAdmin):
    inlines = [
        ModerationReportInline,
    ]
    list_display = ['type', 'object_id', 'description', 'status', 'verified']
    search_fields = ['type']
    class Meta:
            model = Moderation


admin.site.register(Moderation, ModerationAdmin)
