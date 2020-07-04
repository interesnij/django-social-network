from managers.model.user import ModeratedUser, UserModerationReport
from managers.model.community import ModeratedCommunity, CommunityModerationReport
from django import forms


class UserModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedUser
		fields = ['description']

class UserReportForm(forms.ModelForm):
	class Meta:
		model = UserModerationReport
		fields = ['description']


class CommunityModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedCommunity
		fields = ['description']

class CommunityReportForm(forms.ModelForm):
	class Meta:
		model = CommunityModerationReport
		fields = ['description']
