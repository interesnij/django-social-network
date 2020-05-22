from video.models import VideoAlbum, Video
from django import forms


class AlbumForm(forms.ModelForm):

	class Meta:
		model = VideoAlbum
		fields = ['title', 'description', 'is_public']


class VideoForm(forms.ModelForm):

	class Meta:
		model = Video
		fields = ['title', 'description', 'is_public', 'image', 'category', "tag" , 'album', 'is_child', 'comments_enabled', 'uri']
