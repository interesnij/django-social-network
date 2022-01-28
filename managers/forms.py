from django import forms
from managers.models import Moderated, ModerationReport


class ModeratedForm(forms.ModelForm):
	class Meta:
		model = Moderated
		fields = ['description']
class ReportForm(forms.ModelForm):
	class Meta:
		model = ModerationReport
		fields = ['description', 'type']
