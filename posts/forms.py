from posts.models import Post
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		fields = ['content', 'comments_enabled']
