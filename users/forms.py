from django import forms
from users.model.profile import UserProfile, UserDeleted
from users.model.settings import *
from users.models import User


class InfoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('sity', 'status')

class UserNotifyForm(forms.ModelForm):
    class Meta:
        model = UserNotifications
        fields = ('connection_request','connection_confirmed','community_invite',)
class UserNotifyPostForm(forms.ModelForm):
    class Meta:
        model = UserNotificationsPost
        fields = ('comment','comment_reply','comment_mention','mention','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class UserNotifyPhotoForm(forms.ModelForm):
    class Meta:
        model = UserNotificationsPhoto
        fields = ('comment','comment_reply','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class UserNotifyGoodForm(forms.ModelForm):
    class Meta:
        model = UserNotificationsGood
        fields = ('comment','comment_reply','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class UserNotifyVideoForm(forms.ModelForm):
    class Meta:
        model = UserNotificationsVideo
        fields = ('comment','comment_reply','repost','like','dislike','comment_like','comment_dislike','comment_reply_like','comment_reply_dislike',)
class UserNotifyMusicForm(forms.ModelForm):
    class Meta:
        model = UserNotificationsMusic
        fields = ('repost',)

class UserPrivateForm(forms.ModelForm):
	class Meta:
		model = UserPrivate
		fields = (
                'can_see_community',
                'can_see_friends',
                'can_see_message',
                'can_see_post',
                'can_see_photo',
                'can_see_good',
                'can_see_video',
                'can_see_music',
                'can_see_workspaces',
                'can_see_boards',
                )
class UserPrivatePostForm(forms.ModelForm):
	class Meta:
		model = UserPrivatePost
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class UserPrivatePhotoForm(forms.ModelForm):
	class Meta:
		model = UserPrivatePhoto
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class UserPrivateGoodForm(forms.ModelForm):
	class Meta:
		model = UserPrivateGood
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class UserPrivateVideoForm(forms.ModelForm):
	class Meta:
		model = UserPrivateVideo
		fields = ('can_see_comment', 'vote_on', 'add_item', 'add_comment',)
class UserPrivateMusicForm(forms.ModelForm):
	class Meta:
		model = UserPrivateMusic
		fields = ('add_item',)

class UserPrivatePlannerForm(forms.ModelForm):
	class Meta:
		model = UserPrivatePlanner
		fields = ('can_see_comments','add_comments','vote_on',)

class UserNameForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name',)
class UserPasswordForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('password',)
class UserEmailForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email',)
class UserPhoneForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('phone',)

class UserDeletedForm(forms.ModelForm):
	class Meta:
		model = UserDeleted
		fields = ('answer', 'other')
