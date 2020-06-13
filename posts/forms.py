from posts.models import Post, PostComment
from django import forms

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['text']


class PostCommunityForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['text', 'status', 'comments_enabled']


class CommentForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = PostComment
		fields = ['text']
