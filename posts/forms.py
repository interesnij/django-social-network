from posts.models import Post
from django import forms

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['creator', 'views', 'created']
