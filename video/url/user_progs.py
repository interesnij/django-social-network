from django.urls import re_path
from video.view.user_progs import *


urlpatterns = [
    re_path(r'^create_video/(?P<pk>\d+)/$', UserVideoCreate.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$', UserVideoEdit.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', UserVideoDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/$', UserVideoRecover.as_view()),
    re_path(r'^on_comment/(?P<pk>\d+)/$', UserOpenCommentVideo.as_view()),
    re_path(r'^off_comment/(?P<pk>\d+)/$', UserCloseCommentVideo.as_view()),
    re_path(r'^on_private/(?P<pk>\d+)/$', UserOnPrivateVideo.as_view()),
    re_path(r'^off_private/(?P<pk>\d+)/$', UserOffPrivateVideo.as_view()),
    re_path(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesVideo.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesVideo.as_view()),
]
