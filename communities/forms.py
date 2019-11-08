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
        model = UserProfile
        fields = (
            'category',
            'name',
            'description',
            'rules',
            'avatar',
            'cover',
            'status',
        )
