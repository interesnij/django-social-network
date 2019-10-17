from article.models import Article
from django import forms


class ArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['title', 'content', 'image', 'comments_enabled']


class ArticleRepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)
