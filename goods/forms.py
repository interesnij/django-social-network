from goods.models import Good, GoodComment, GoodList
from django import forms


class GoodForm(forms.ModelForm):

	class Meta:
		model = Good
		fields = ['title', 'image', 'price', 'description', ]

class CommentForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = GoodComment
		fields = ['text']

class GoodListForm(forms.ModelForm):
	class Meta:
		model = GoodList
		fields = ['title', 'order', ]
