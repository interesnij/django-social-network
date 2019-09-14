from django import forms
from django.http import Http404
from users.models import User
from django import forms

class GeneralUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False,max_length=256,label='Имя')
    last_name = forms.CharField(required=False,max_length=256,label='Фамилия')

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
