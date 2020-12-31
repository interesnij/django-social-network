from django.contrib import admin
from survey.models import *


class AnswerInline(admin.TabularInline):
    model = Answer

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'community', 'is_anonymous', 'is_multiple', 'is_no_edited', 'time_end']
    inlines = [
        AnswerInline,
    ]
    search_fields = ('title',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyVote)
