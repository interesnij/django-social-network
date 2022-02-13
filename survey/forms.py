from django import forms
from survey.models import Survey, SurveyList


class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = [
			"title",
			"image",
			"is_anonymous",
			"is_multiple",
			"is_no_edited",
			"is_no_edited",
		]

class SurveyListForm(forms.ModelForm):
	class Meta:
		model = SurveyList
		fields = ['name', 'description']
