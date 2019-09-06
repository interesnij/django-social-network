from posts.models import Post
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostHardForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['content_hard']

class PostMediumForm(forms.ModelForm):


	class Meta:
		model = Post
		fields = ['']

class PostLiteForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['content_lite']
