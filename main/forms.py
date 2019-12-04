from django import forms
from main.models import ItemComment, ItemCommentPhoto


class CommentForm(forms.ModelForm):

	class Meta:
		model = ItemComment
		fields = ['text', 'item_comment_photo', 'item_comment_photo2']
