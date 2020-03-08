from django import forms
from users.models import User
from users.model.profile import UserProfile
from users.model.settings import UserItemPrivate, UserItemNotifications


class GeneralUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False,max_length=256,label='Имя')
    last_name = forms.CharField(required=False,max_length=256,label='Фамилия')

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','sity','vk_url','youtube_url','facebook_url','instagram_url','twitter_url','phone',)


class AboutUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('bio',)


class SettingsPrivateForm(forms.ModelForm):

    class Meta:
        model = UserItemPrivate
        fields = (
            'is_private',
            'can_message',
            'photo_visible_all',
            'photo_visible_frends',
            'can_comments',
            'can_add_post',
            'can_add_article',
            'can_add_good',
        )

class SettingsNotifyForm(forms.ModelForm):

    class Meta:
        model = UserItemNotifications
        fields = (
            'comment_notifications',
            'comment_reply_notifications',
            'comment_user_mention_notifications',
            'user_mention_notifications',
            'repost_notifications',
            'like_notifications',
            'dislike_notifications',
            'comment_like_notifications',
            'comment_dislike_notifications',
            'comment_reply_like_notifications',
            'comment_reply_dislike_notifications',
        )
