from video.models import VideoList, Video, VideoComment
from django import forms


class VideoListForm(forms.ModelForm):
	class Meta:
		model = VideoList
		fields = ['name', 'description']

class VideoUploadForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ['uri', 'file']


class VideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = [
			'title',
			'description',
			'image',
			'votes_on',
			'comments_enabled',
			]

class EditVideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ['title', 'description', 'image', 'votes_on', 'comments_enabled']
