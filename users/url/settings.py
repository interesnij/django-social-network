from django.conf.urls import url
from users.views.settings import *


urlpatterns = [
    url(r'^general/$', UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^info/$', UserInfoChange.as_view(), name='user_info_form'),
    url(r'^design/$', UserDesign.as_view(), name='user_design_form'),

    url(r'^notify/$', UserNotifyView.as_view(), name='user_profile_notify'),
    url(r'^notify_post/$', UserNotifyPostView.as_view(), name='user_post_notify'),
    url(r'^notify_photo/$', UserNotifyPhotoView.as_view(), name='user_photo_notify'),
    url(r'^notify_good/$', UserNotifyGoodView.as_view(), name='user_good_notify'),
    url(r'^notify_video/$', UserNotifyVideoView.as_view(), name='user_video_notify'),
    url(r'^notify_music/$', UserNotifyMusicView.as_view(), name='user_music_notify'),

    url(r'^private/$', UserPrivateView.as_view(), name='user_profile_private'),
    url(r'^private_post/$', UserPrivatePostView.as_view(), name='user_post_private'),
    url(r'^private_photo/$', UserPrivatePhotoView.as_view(), name='user_photo_private'),
    url(r'^private_good/$', UserPrivateGoodView.as_view(), name='user_good_private'),
    url(r'^private_video/$', UserPrivateVideoView.as_view(), name='user_video_private'),
    url(r'^private_music/$', UserPrivateMusicView.as_view(), name='user_music_private'),
]
