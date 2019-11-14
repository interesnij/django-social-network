from django import forms
from main.models import ItemComment
from posts.models import Post

class CommentForm(forms.ModelForm):

	class Meta:
		model = ItemComment
		fields = ['text']
