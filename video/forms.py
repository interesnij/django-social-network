from video.models import VideoAlbum
from django import forms


class AlbumForm(forms.ModelForm):

	class Meta:
		model = VideoAlbum
		fields = ['title', 'description', 'is_public']
