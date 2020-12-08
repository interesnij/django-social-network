from posts.models import *
from django import forms

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['text']


class CommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = PostComment
		fields = ['text']


class PostListForm(forms.ModelForm):
	class Meta:
		model = PostList
		fields = ['name','type', 'order',]
