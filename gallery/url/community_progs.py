from gallery.view.community_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^description/(?P<pk>\d+)/$', CommunityPhotoDescription.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', CommunityPhotoDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', CommunityPhotoRecover.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentPhoto.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentPhoto.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesPhoto.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesPhoto.as_view()),
	url(r'^add_avatar/(?P<pk>\d+)/$', CommunityAddAvatar.as_view()),
]
