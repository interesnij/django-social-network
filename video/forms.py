from video.models import VideoAlbum, Video, VideoComment
from django import forms


class AlbumForm(forms.ModelForm):

	class Meta:
		model = VideoAlbum
		fields = ['title', 'is_public', 'order']


class VideoForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	class Meta:
		model = Video
		fields = ['title', 'description', 'is_public', 'image', 'category', 'album', 'is_child', 'comments_enabled', 'uri']

class CommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = VideoComment
		fields = ['text']
