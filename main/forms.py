from django import forms
from main.models import ItemCommentPhoto


class CommentForm(forms.ModelForm):
	text = forms.CharField(required=False,max_length=500,label='Текст')

	class Meta:
		model = ItemCommentPhoto
		fields = ['item_comment_photo', 'item_comment_photo2', 'text']
