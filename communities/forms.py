from communities.models import Community
from django import forms


class GoodForm(forms.ModelForm):

	class Meta:
		model = Community
		fields = [	'title',
					'type',
				]
