from django import forms
from django.http import Http404
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms

class GeneralUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False,max_length=256,label='Имя')
    last_name = forms.CharField(required=False,max_length=256,label='Фамилия')

    class Meta:
        model = UserProfile
        fields = (
        'first_name',
        'last_name',
        'sity',
        'vk_url',
        'youtube_url',
        'facebook_url',
        'instagram_url',
        'twitter_url',
        'phone',
        )
    def __init__(self, *args, **kwargs):
        super(GeneralUserForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        except User.DoesNotExist:
            raise Http404

        return

class AboutUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
        'bio',
        )
