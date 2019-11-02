from article.models import Article
from django import forms


class ArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['title', 'content', 'g_image', 'comments_enabled']
