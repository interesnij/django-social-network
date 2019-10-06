from django.contrib import admin
from django.contrib.admin import ModelAdmin
from moderation.models import ModerationCategory, ModerationReport, ModeratedObject


admin.site.register(ModerationCategory)



class ModerationReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    readonly_fields = ['reporter', 'moderated_object', 'category', 'description']


admin.site.register(ModerationReport, ModerationReportAdmin)


class ModeratedObjectAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    readonly_fields = ['verified', 'category', 'description', 'community', 'status', 'object_type', 'object_id', 'content_type']


admin.site.register(ModeratedObject, ModeratedObjectAdmin)
