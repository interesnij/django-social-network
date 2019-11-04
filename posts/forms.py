from posts.models import Post
from django import forms

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['text', 'status', 'comments_enabled']


class PostCommunityForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['text', 'status', 'comments_enabled', 'community']
