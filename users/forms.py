from django import forms
from django.http import Http404
from django.contrib.auth.models import User
from .models import UserProfile, UserPrivateSettings, UserNotificationsSettings
from django import forms
from gallery.models import Photo


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
            'comment_reply_notifications',
            'connection_request_notifications',
            'connection_confirmed_notifications',
            'community_invite_notifications',
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
