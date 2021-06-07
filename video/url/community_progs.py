from django.conf.urls import url
from video.view.community_progs import *


urlpatterns = [
    url(r'^create_video/(?P<pk>\d+)/$', CommunityVideoCreate.as_view()),
    url(r'^edit/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoEdit.as_view()),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoDelete.as_view()),
    url(r'^restore/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoRecover.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', CommunityOpenCommentVideo.as_view()),
    url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', CommunityCloseCommentVideo.as_view()),
    url(r'^on_private/(?P<uuid>[0-9a-f-]+)/$', CommunityOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<uuid>[0-9a-f-]+)/$', CommunityOffPrivateVideo.as_view()),
    url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesVideo.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesVideo.as_view()),
    url(r'^add_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddVideoInCommunityList.as_view()),
    url(r'^remove_video_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveVideoFromCommunityList.as_view()),

    url(r'^post-comment/$', VideoCommentCommunityCreate.as_view()),
    url(r'^reply-comment/$', VideoReplyCommunityCreate.as_view()),
    url(r'^delete_comment/(?P<pk>\d+)/$', VideoCommentCommunityDelete.as_view()),
	url(r'^restore_comment/(?P<pk>\d+)/$', VideoCommentCommunityRecover.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', CommunityVideoListCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', CommunityVideolistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', CommunityVideolistDelete.as_view()),
    url(r'^restore_list/(?P<uuid>[0-9a-f-]+)/$', CommunityVideolistRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddVideoListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveVideoListFromCommunityCollections.as_view()),
]
