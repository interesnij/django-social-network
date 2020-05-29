from django.contrib import admin
from quan.models import QuestionsCategory, Question, QuestionVote

admin.site.register(QuestionsCategory)
admin.site.register(Question)
admin.site.register(QuestionVote)
