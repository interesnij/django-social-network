from django import forms
from main.models import ItemComment


class CommentForm(forms.ModelForm):
	item_comment_photo = forms.ImageField(required=False)
	item_comment_photo2 = forms.ImageField(required=False)
	text=forms.CharField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control text-comment form-control-rounded'}
        ))

	class Meta:
		model = ItemComment
		fields = ['text']


class CommentReplyForm(forms.ModelForm):

	item_comment_photo = forms.FileField()
	item_comment_photo2 = forms.FileField()
	text=forms.CharField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control text-comment form-control-rounded'}
        ))

	class Meta:
		model = ItemComment
		fields = ['text', 'item_comment_photo', 'item_comment_photo2']
