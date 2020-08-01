from django.conf.urls import url
from users.views.settings import *


urlpatterns = [
    url(r'^general/(?P<pk>[0-9]+)/$', UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^info/(?P<pk>[0-9]+)/$', UserInfoChange.as_view(), name='user_info_form'),
    url(r'^design/(?P<pk>\d+)/$', UserDesign.as_view(), name='user_design_form'),

    url(r'^notify/(?P<pk>[0-9]+)/$', UserNotifyView.as_view(), name='user_profile_notify'),
    url(r'^notify_post/(?P<pk>[0-9]+)/$', UserNotifyPostView.as_view(), name='user_post_notify'),
    url(r'^notify_photo/(?P<pk>[0-9]+)/$', UserNotifyPhotoView.as_view(), name='user_photo_notify'),
    url(r'^notify_good/(?P<pk>[0-9]+)/$', UserNotifyGoodView.as_view(), name='user_good_notify'),
    url(r'^notify_video/(?P<pk>[0-9]+)/$', UserNotifyVideoView.as_view(), name='user_video_notify'),
    url(r'^notify_music/(?P<pk>[0-9]+)/$', UserNotifyMusicView.as_view(), name='user_music_notify'),

    url(r'^private/(?P<pk>[0-9]+)/$', UserPrivateView.as_view(), name='user_profile_private'),
    url(r'^private_post/(?P<pk>[0-9]+)/$', UserPrivatePostView.as_view(), name='user_post_private'),
    url(r'^private_photo/(?P<pk>[0-9]+)/$', UserPrivatePhotoView.as_view(), name='user_photo_private'),
    url(r'^private_good/(?P<pk>[0-9]+)/$', UserPrivateGoodView.as_view(), name='user_good_private'),
    url(r'^private_video/(?P<pk>[0-9]+)/$', UserPrivateVideoView.as_view(), name='user_video_private'),
    url(r'^private_music/(?P<pk>[0-9]+)/$', UserPrivateMusicView.as_view(), name='user_music_private'),
]
