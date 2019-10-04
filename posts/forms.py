from posts.models import Post,PostComment
from django import forms


class PostCommentForm(forms.ModelForm):

	class Meta:
		model = PostComment
		fields = ['text']

class RepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)
