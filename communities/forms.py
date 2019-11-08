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

	class Meta:
		model = Community
		fields = ['name', 'description', 'rules', 'status',]


class AvatarCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['avatar', ]


class CoverCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['cover', ]


class CatCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['category', ]
