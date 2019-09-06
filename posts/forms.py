from posts.models import Post
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		exclude = ['creator', 'views', 'created']
