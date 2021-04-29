from video.models import VideoList, Video, VideoComment
from django import forms


class VideoListForm(forms.ModelForm):
	class Meta:
		model = VideoList
		fields = ['name', 'description', 'order']


class VideoForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder':'Описание'}))
	class Meta:
		model = Video
		fields = ['title', 'description', 'image', 'list', 'comments_enabled', 'uri']

class CommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = VideoComment
		fields = ['text']
