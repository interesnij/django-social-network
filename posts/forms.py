from posts.models import Post
from django import forms

class BlogForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['creator', 'views', 'created']
