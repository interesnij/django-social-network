from django import forms
from blog.models import BlogComment

class CommentForm(forms.ModelForm):

	class Meta:
		model = ArticleComment
		fields = ['text']
