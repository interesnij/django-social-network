from managers.model.user import ModeratedUser, UserModerationReport
from django import forms


class UserModeratedForm(forms.ModelForm):

	class Meta:
		model = ModeratedUser
		fields = ['description']

class UserReportForm(forms.ModelForm):

	class Meta:
		model = UserModerationReport
		fields = ['description']
