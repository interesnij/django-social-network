from django.conf.urls import url
from video.view.community_progs import *


urlpatterns = [
    #url(r'^create_video/(?P<pk>\d+)/$', CommunityVideoCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', CommunityVideoEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', CommunityVideoDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', CommunityVideoRecover.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentVideo.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentVideo.as_view()),
    url(r'^on_private/(?P<pk>\d+)/$', CommunityOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<pk>\d+)/$', CommunityOffPrivateVideo.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesVideo.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesVideo.as_view()),
]
