from music.models import SoundList, Music
from django import forms


class PlaylistForm(forms.ModelForm):

	class Meta:
		model = SoundList
		fields = ['name', 'order', 'description']

class TrackForm(forms.ModelForm):

	class Meta:
		model = Music
		fields = ['title', 'file', 'list', ]
