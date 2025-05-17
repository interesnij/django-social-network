from gallery.view.community_progs import *
from django.urls import re_path


urlpatterns=[
    re_path(r'^description/(?P<pk>\d+)/$', CommunityPhotoDescription.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', CommunityPhotoDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/$', CommunityPhotoRecover.as_view()),
    re_path(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentPhoto.as_view()),
    re_path(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentPhoto.as_view()),
    re_path(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesPhoto.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesPhoto.as_view()),
	re_path(r'^add_avatar/(?P<pk>\d+)/$', CommunityAddAvatar.as_view()),
]
