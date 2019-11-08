from django import forms
from django.http import Http404
from django.contrib.auth.models import User
from .models import UserProfile, UserPrivateSettings, UserNotificationsSettings
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


class AboutUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'bio',
        )

class AvatarUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'avatar',
        )

class SettingsPrivateForm(forms.ModelForm):

    class Meta:
        model = UserPrivateSettings
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
        model = UserNotificationsSettings
        fields = (
            'comment_notifications',
            'react_notifications',
            'comment_reply_notifications',
            'comment_reply_react_notifications',
            'comment_react_notifications',
            'connection_request_notifications',
            'connection_confirmed_notifications',
            'community_invite_notifications',
            'comment_user_mention_notifications',
            'user_mention_notifications',
            'repost_notifications',
        )
