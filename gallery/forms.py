from django import forms
from guestbook.models import Guestbook

class GuestbookForm(forms.ModelForm):
	content = forms.CharField(
        label="",widget=forms.Textarea(
                attrs={'class': 'input-md round form-control', 'placeholder': 'Напишите отзыв','rows':'0','cols':'0','style':'height: 84px;'}
            )
    )
	class Meta:
		model=Guestbook
		exclude=['user', ]
