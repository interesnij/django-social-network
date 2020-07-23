from goods.models import Good, GoodComment
from django import forms


class GoodForm(forms.ModelForm):

	class Meta:
		model = Good
		fields = [	'image',
					'image2',
					'image3',
					'image4',
					'image5',
				]

class CommentForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = GoodComment
		fields = ['text']
