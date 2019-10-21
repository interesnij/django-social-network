from article.models import Article
from django import forms


class ArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['title', 'content', 'image', 'comments_enabled']
