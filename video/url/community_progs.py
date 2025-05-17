from django.urls import re_path
from video.view.community_progs import *


urlpatterns = [
    #url(r'^create_video/(?P<pk>\d+)/$', CommunityVideoCreate.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$', CommunityVideoEdit.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', CommunityVideoDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/$', CommunityVideoRecover.as_view()),
    re_path(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentVideo.as_view()),
    re_path(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentVideo.as_view()),
    re_path(r'^on_private/(?P<pk>\d+)/$', CommunityOnPrivateVideo.as_view()),
    re_path(r'^off_private/(?P<pk>\d+)/$', CommunityOffPrivateVideo.as_view()),
    re_path(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesVideo.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesVideo.as_view()),
]
