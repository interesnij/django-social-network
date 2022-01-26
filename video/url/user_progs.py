from django.conf.urls import url
from video.view.user_progs import *


urlpatterns = [
    url(r'^create_video/(?P<pk>\d+)/$', UserVideoCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', UserVideoEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', UserVideoDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', UserVideoRecover.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', UserOpenCommentVideo.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', UserCloseCommentVideo.as_view()),
    url(r'^on_private/(?P<pk>\d+)/$', UserOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<pk>\d+)/$', UserOffPrivateVideo.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesVideo.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesVideo.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', UserChangeVideoPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangeVideoListPosition.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', UserVideolistEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', UserVideolistDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', UserVideolistRecover.as_view()),
    url(r'^add_list_in_collections/(?P<list_pk>\d+)/$', AddVideoListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<list_pk>\d+)/$', RemoveVideoListFromUserCollections.as_view()),
]
