from django import forms
from users.model.profile import UserProfile
from users.model.settings import UserPrivate, UserPostNotifications


class InfoUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False,max_length=256,label='Имя')
    last_name = forms.CharField(required=False,max_length=256,label='Фамилия')

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','sity')


class SettingsPrivateForm(forms.ModelForm):

    class Meta:
        model = UserPrivate
        fields = (
            'is_private',
            'open_message',
            'open_wall',
            'open_good',
            'open_video',
        )

class SettingsNotifyForm(forms.ModelForm):

    class Meta:
        model = UserPostNotifications
        fields = (
            'comment',
            'comment_reply',
            'comment_mention',
            'mention',
            'repost',
            'like',
            'dislike',
            'comment_like',
            'comment_dislike',
            'comment_reply_like',
            'comment_reply_dislike',
        )
