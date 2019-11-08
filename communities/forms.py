from communities.models import Community
from django import forms


class CommunityForm(forms.ModelForm):

	class Meta:
		model = Community
		fields = [	'name',
					'type',
					'category',
					'id',
				]

class GeneralCommunityForm(forms.ModelForm):
	description = forms.CharField( label="",widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '5'}
        ))
	class Meta:
		model = Community
		fields = 'category', 'name', 'description', 'rules', 'avatar', 'cover', 'status'
