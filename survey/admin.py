from django.contrib import admin
from survey.models import *


class AnswerInline(admin.TabularInline):
    model = Answer
class VoteInline(admin.TabularInline):
    model = SurveyVote

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_anonymous', 'is_multiple', 'is_no_edited', 'time_end']
    inlines = [
        AnswerInline,
        VoteInline,
    ]
    search_fields = ('title',)

class SurveyListAdmin(admin.ModelAdmin):
    search_fields = ('creator',)
    list_display = ['name','type','creator', 'community']

admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyList, SurveyListAdmin)
