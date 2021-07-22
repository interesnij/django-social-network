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


class CoverCommunityForm(forms.ModelForm):
	class Meta:
		model = CommunityInfo
		fields = ['description', ]


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

class CommunityPrivatePostForm(forms.ModelForm):
	class Meta:
		model = CommunityPrivatePost
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class CommunityPrivatePhotoForm(forms.ModelForm):
	class Meta:
		model = CommunityPrivatePhoto
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class CommunityPrivateGoodForm(forms.ModelForm):
	class Meta:
		model = CommunityPrivateGood
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class CommunityPrivateVideoForm(forms.ModelForm):
	class Meta:
		model = CommunityPrivateVideo
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class CommunityPrivateMusicForm(forms.ModelForm):
	class Meta:
		model = CommunityPrivateMusic
		fields = ('add_item',)

class CommunitySectionOpenForm(forms.ModelForm):
	class Meta:
		model = CommunitySectionsOpen
		fields = (
                'can_see_members', 
                'can_receive_message',
                'can_see_post',
                'can_see_photo',
                'can_see_good',
                'can_see_video',
                'can_see_music',
                'can_see_workspace',
                'can_see_board',
				'can_see_doc',
                )
