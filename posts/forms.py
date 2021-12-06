from posts.models import *
from django import forms

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['text', 'category', 'comments_enabled', 'is_signature', 'votes_on',]


class CommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = PostComment
		fields = ['text']


class PostsListCreateForm(forms.ModelForm):
	class Meta:
		model = PostsList
		fields = ['name', 'description','can_see_el','can_see_comment','create_el','create_comment', 'copy_el']

class PostsListEditForm(forms.ModelForm):
	class Meta:
		model = PostsList
		fields = ['name', 'description',]
