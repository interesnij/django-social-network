from communities.models import *
from communities.model.settings import *
from django import forms


class CommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['name','type','category','id', ]


class GeneralCommunityForm(forms.ModelForm):
	name = forms.CharField( label="",widget=forms.TextInput(attrs={'class': 'form-control'}))
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	status = forms.CharField( label="",required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	class Meta:
		model = Community
		fields = ['name', 'description', 'status',]


class CoverCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['cover', ]


class CatCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['category', ]


class CommunityNotifyForm(forms.ModelForm):
    class Meta:
        model = CommunityNotificationsSettings
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

class CommunityPrivateForm(forms.ModelForm):
    class Meta:
        model = CommunityPrivateSettings
        fields = (
            'photo_visible_all',
            'photo_visible_member',
            'can_comments',
            'can_add_post',
            'can_add_article',
            'can_add_good',
        )
