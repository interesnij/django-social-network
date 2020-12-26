from django.contrib import admin
from survey.models import *


admin.site.register(Survey)
admin.site.register(Answer)
admin.site.register(SurveyVote)
