from django import forms
from users.model.profile import UserProfile
from users.model.settings import *


class InfoUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False,max_length=256,label='Имя')
    last_name = forms.CharField(required=False,max_length=256,label='Фамилия')

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','sity')

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

class UserPrivatePostForm(forms.ModelForm):
	class Meta:
		model = UserPrivatePost
		fields = ('wall', 'comment',)
class UserPrivatePhotoForm(forms.ModelForm):
	class Meta:
		model = UserPrivatePhoto
		fields = ('photo', 'comment',)
class UserPrivateGoodForm(forms.ModelForm):
	class Meta:
		model = UserPrivateGood
		fields = ('good', 'comment',)
class UserPrivateVideoForm(forms.ModelForm):
	class Meta:
		model = UserPrivateVideo
		fields = ('video', 'comment',)
class UserPrivateMusicForm(forms.ModelForm):
	class Meta:
		model = UserPrivateMusic
		fields = ('music',)
