from django import forms
from survey.models import Survey


class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = ['title']
