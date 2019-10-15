from article.models import Article,ArticleComment
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = ['title', 'content', 'image', 'comments_enabled']

class ArticleCommentForm(forms.ModelForm):

	class Meta:
		model = ArticleComment
		fields = ['text']

class ArticleRepostForm(forms.Form):
    repost_comment = forms.CharField(widget=forms.Textarea)
