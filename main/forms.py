from django import forms
from main.models import ItemComment, ItemCommentPhoto


class CommentForm(forms.ModelForm):
	item_comment_photo = forms.FileField()
	item_comment_photo2 = forms.FileField()

	class Meta:
		model = ItemComment
		fields = ['text']
