from posts.models import Post
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostHardForm(forms.ModelForm):
	content_hard = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		exclude = ['views', 'creator', 'communities', 'is_closed', 'is_deleted', 'content_medium', 'content_lite']

class PostMediumForm(forms.ModelForm):
	content_medium = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		exclude = ['views', 'creator', 'communities', 'is_closed', 'is_deleted', 'content_hard', 'content_lite']

class PostLiteForm(forms.ModelForm):
	content_lite = forms.CharField(widget=CKEditorUploadingWidget, label='')

	class Meta:
		model = Post
		exclude = ['views', 'creator', 'communities', 'is_closed', 'is_deleted', 'content_medium', 'content_hard']
