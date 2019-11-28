from gallery.models import Album, Photo
from django import forms


class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		fields = ['title','description','is_public','order', ]


class AvatarUserForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = (
            'file',
        )


class AvatarCommunityForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['avatar', ]
