from posts.models import Post
from django import forms
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorWidget, label='')

	class Meta:
		model = Post
		exclude = ['creator', 'views', 'created']
