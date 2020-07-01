from managers.model.user import ModeratedUser
from django import forms


class UserModeratedForm(forms.ModelForm):
	
	class Meta:
		model = ModeratedUser
		fields = ['description']
