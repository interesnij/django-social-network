from gallery.models import Album
from django import forms


class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		fields = ['title','description','is_public','order', ]
