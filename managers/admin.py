from django.contrib import admin
from managers.models import ModerationReport


class ModerationReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'description', 'type']
    search_fields = ['type']
    class Meta:
            model = ModerationReport


admin.site.register(ModerationReport, ModerationReportAdmin)
