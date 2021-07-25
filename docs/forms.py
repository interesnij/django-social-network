from docs.models import DocList, Doc
from django import forms
from django.conf import settings


class DoclistForm(forms.ModelForm):

	class Meta:
		model = DocList
		fields = ['name', 'description','can_see_item','can_see_comment','add_item','add_comment','can_copy_item','can_copy_list',]

class DocForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

	class Meta:
		model = Doc
		fields = ['title', 'file', 'list', 'type_2',]
