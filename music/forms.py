from music.models import MusicList, Music
from django import forms


class PlaylistForm(forms.ModelForm):

	class Meta:
		model = MusicList
		fields = ['name', 'description']

class TrackForm(forms.ModelForm):

	class Meta:
		model = Music
		fields = ['title', 'file', 'list', ]
