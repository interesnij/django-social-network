from communities.models import *
from communities.model.settings import *
from django import forms


class CommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['name','type','category',]


class GeneralCommunityForm(forms.ModelForm):
	name = forms.CharField( label="",widget=forms.TextInput(attrs={'class': 'form-control'}))
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	status = forms.CharField( label="",required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	class Meta:
		model = Community
		fields = ['name', 'status', 'category',]


class CatCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['category', ]


class CommunityNotifyPostForm(forms.ModelForm):
    class Meta:
        model = CommunityNotificationsPost
        fields = ('comment','comment_reply','comment_mention','mention','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class CommunityNotifyPhotoForm(forms.ModelForm):
    class Meta:
        model = CommunityNotificationsPhoto
        fields = ('comment','comment_reply','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class CommunityNotifyGoodForm(forms.ModelForm):
    class Meta:
        model = CommunityNotificationsGood
        fields = ('comment','comment_reply','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class CommunityNotifyVideoForm(forms.ModelForm):
    class Meta:
        model = CommunityNotificationsVideo
        fields = ('comment','comment_reply','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class CommunityNotifyMusicForm(forms.ModelForm):
    class Meta:
        model = CommunityNotificationsMusic
        fields = ('repost',)
