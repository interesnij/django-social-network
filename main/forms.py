from django import forms
from main.models import ItemComment


class CommentForm(forms.ModelForm):
	photo = forms.ImageField(required=False)
	photo2 = forms.ImageField(required=False)
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = ItemComment
		fields = ['text']
