from goods.models import Good
from django import forms


class GoodForm(forms.ModelForm):

	class Meta:
		model = Good
		fields = ['title', 'sub_category', 'price', 'description', 'image', 'comments_enabled']
