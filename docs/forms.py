from docs.models import DocList
from django import forms


class DoclistForm(forms.ModelForm):

	class Meta:
		model = DocList
		fields = ['name', 'is_public', 'order']
