from music.models import SoundList
from django import forms


class PlaylistForm(forms.ModelForm):

	class Meta:
		model = SoundList
		fields = ['name', 'order']
