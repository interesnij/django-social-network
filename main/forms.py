from django import forms
from blog.models import BlogComment

class CommentForm(forms.Form):
    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    comment_area = forms.CharField(
        label="",widget=forms.Textarea(
                attrs={'class': 'form-field', 'placeholder': 'Напишите что-нибудь','rows':'0','cols':'0'}
            )
    )
