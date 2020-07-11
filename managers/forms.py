from django import forms
from managers.model.user import ModeratedUser, UserModerationReport
from managers.model.community import ModeratedCommunity, CommunityModerationReport
from managers.model.post import *
from managers.model.good import *
from managers.model.photo import *
from managers.model.video import *
from managers.model.audio import *
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

class PostModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedPost
		fields = ['description']
class PostReportForm(forms.ModelForm):
	class Meta:
		model = PostModerationReport
		fields = ['description']
class PostCommentModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedPostComment
		fields = ['description']
class PostCommentReportForm(forms.ModelForm):
	class Meta:
		model = PostCommentModerationReport
		fields = ['description']

class PhotoModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedPhoto
		fields = ['description']
class PhotoReportForm(forms.ModelForm):
	class Meta:
		model = PhotoModerationReport
		fields = ['description']
class PhotoCommentModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedPhotoComment
		fields = ['description']
class PhotoCommentReportForm(forms.ModelForm):
	class Meta:
		model = PhotoCommentModerationReport
		fields = ['description']

class VideoModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedVideo
		fields = ['description']
class VideoReportForm(forms.ModelForm):
	class Meta:
		model = VideoModerationReport
		fields = ['description']
class VideoCommentModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedVideoComment
		fields = ['description']
class VideoCommentReportForm(forms.ModelForm):
	class Meta:
		model = VideoCommentModerationReport
		fields = ['description']

class GoodModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedGood
		fields = ['description']
class GoodReportForm(forms.ModelForm):
	class Meta:
		model = GoodModerationReport
		fields = ['description']
class GoodCommentModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedGoodComment
		fields = ['description']
class GoodCommentReportForm(forms.ModelForm):
	class Meta:
		model = GoodCommentModerationReport
		fields = ['description']

class AudioModeratedForm(forms.ModelForm):
	class Meta:
		model = ModeratedAudio
		fields = ['description']
class AudioReportForm(forms.ModelForm):
	class Meta:
		model = AudioModerationReport
		fields = ['description']
