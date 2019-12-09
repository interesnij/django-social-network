from django import forms
from main.models import ItemComment


class CommentForm(forms.ModelForm):

	text=forms.CharField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control text-comment form-control-rounded'}
        ))

	class Meta:
		model = ItemComment
		fields = ['text', 'item_comment_photo', 'item_comment_photo2']


class CommentReplyForm(forms.ModelForm):

	text=forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control text-comment form-control-rounded'}
        ))

	class Meta:
		model = ItemComment
		fields = ['text', 'item_comment_photo', 'item_comment_photo2']
