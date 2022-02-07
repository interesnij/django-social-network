from docs.models import DocsList, Doc
from django import forms
from django.conf import settings


class DocListForm(forms.ModelForm):

	class Meta:
		model = DocsList
		fields = ['name', 'description',]

class DocForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

	class Meta:
		model = Doc
		fields = ['title', 'type_2',]
