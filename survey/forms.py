from django import forms
from survey.models import Survey, SurveyList


class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = ['title']

class SurveyListForm(forms.ModelForm):
	class Meta:
		model = SurveyList
		fields = ['name', 'order', 'description']
