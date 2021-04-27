from gallery.models import PhotoList, Photo, PhotoComment
from django import forms


class PhotoListForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	class Meta:
		model = PhotoList
		fields = ['name', 'description', 'is_public', 'order', ]

class PhotoDescriptionForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: auto;', 'rows': '4'}))
	class Meta:
		model = Photo
		fields = ['description',]

class AvatarCommunityForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['file', ]

class CommentForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = PhotoComment
		fields = ['text']
