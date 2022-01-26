from django.conf.urls import url
from video.view.community_progs import *


urlpatterns = [
    url(r'^create_video/(?P<pk>\d+)/$', CommunityVideoCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', CommunityVideoEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', CommunityVideoDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', CommunityVideoRecover.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentVideo.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentVideo.as_view()),
    url(r'^on_private/(?P<pk>\d+)/$', CommunityOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<pk>\d+)/$', CommunityOffPrivateVideo.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesVideo.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesVideo.as_view()),

    url(r'^delete_comment/(?P<pk>\d+)/$', VideoCommentCommunityDelete.as_view()),
	url(r'^restore_comment/(?P<pk>\d+)/$', VideoCommentCommunityRecover.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', CommunityVideoListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', CommunityVideolistEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', CommunityVideolistDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', CommunityVideolistRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', AddVideoListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', RemoveVideoListFromCommunityCollections.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', CommunityChangeVideoPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', CommunityChangeVideoListPosition.as_view()),
]
