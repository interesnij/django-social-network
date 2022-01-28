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


admin.site.register(Moderated, ModeratedAdmin)
