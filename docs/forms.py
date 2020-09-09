from docs.models import DocList, Doc
from django import forms


class DoclistForm(forms.ModelForm):

	class Meta:
		model = DocList
		fields = ['name', 'is_public', 'order']

class DocForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	class Meta:
		model = Doc
		fields = ['title', 'file', 'type', 'list', ]
