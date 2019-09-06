from posts.models import Post
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostHardForm(forms.ModelForm):
	content_hard = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		fields = ['content_hard', 'comments_enabled']

class PostMediumForm(forms.ModelForm):
	content_medium = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		fields = ['content_medium', 'comments_enabled']

class PostLiteForm(forms.ModelForm):
	content_lite = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		fields = ['content_lite', 'comments_enabled']
