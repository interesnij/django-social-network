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
					'price',
					'description',
					'comments_enabled',
					'votes_on',
					'sub_category',
				]

class CommentForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = GoodComment
		fields = ['text']
