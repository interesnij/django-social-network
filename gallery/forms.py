from gallery.models import Album, Photo
from django import forms


class AlbumForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	class Meta:
		model = Album
		fields = ['title', 'description', 'is_public', 'order', ]


class AvatarUserForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['file',]

class PhotoDescriptionForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: auto;', 'rows': '4'}))
	class Meta:
		model = Photo
		fields = ['description',]


class AvatarCommunityForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['file', ]
