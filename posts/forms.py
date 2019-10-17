from posts.models import Post
from django import forms


class PostRepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)

class PostUserForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['text']
