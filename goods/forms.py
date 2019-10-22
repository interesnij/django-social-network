from goods.models import Good
from django import forms


class GoodForm(forms.ModelForm):

	class Meta:
		model = Good
		fields = [	'title',
					'sub_category',
					'price',
					'description',
					'image',
					'image2',
					'image3',
					'image4', 
					'image5',
					'comments_enabled'
				]
