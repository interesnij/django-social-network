from posts.models import Post
from django import forms


class PostRepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['text','image']
