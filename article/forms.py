from article.models import Article,ArticleComment
from django import forms


class ArticleHardForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['content_hard']

class ArticleMediumForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['content_medium']

class ArticleLiteForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['content_lite']

class ArticleCommentForm(forms.ModelForm):

	class Meta:
		model = ArticleComment
		fields = ['text']

class ArticleRepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)
