from article.models import Article,ArticleComment
from django import forms


class ArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['content_hard']

class ArticleCommentForm(forms.ModelForm):

	class Meta:
		model = ArticleComment
		fields = ['text']

class ArticleRepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)
