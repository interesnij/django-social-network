from communities.models import Community, CommunityNotificationsSettings
from django import forms


class CommunityForm(forms.ModelForm):

	class Meta:
		model = Community
		fields = [	'name',
					'type',
					'category',
					'id',
				]

class GeneralCommunityForm(forms.ModelForm):

	class Meta:
		model = Community
		fields = ['name', 'description', 'rules', 'status',]


class AvatarCommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['avatar', ]


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
            'comment_notifications',
            'react_notifications',
            'comment_reply_notifications',
            'comment_reply_react_notifications',
            'comment_react_notifications',
            'connection_request_notifications', 
            'comment_user_mention_notifications',
            'user_mention_notifications',
            'repost_notifications',
        )
