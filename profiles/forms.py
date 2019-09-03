from django import forms
from django.http import Http404
from .models import UserProfile
from django import forms

class IdentiteForm(forms.ModelForm):
    first_name = forms.CharField(required=False,max_length=256,label='Имя')
    last_name = forms.CharField(required=False,max_length=256,label='Фамилия')

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super(IdentiteForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        except User.DoesNotExist:
            raise Http404

        return
