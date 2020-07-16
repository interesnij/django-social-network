from django.conf.urls import url
from video.view.user_progs import *


urlpatterns = [
    url(r'^create_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
    url(r'^create_video_attach/(?P<pk>\d+)/$', UserVideoAttachCreate.as_view()),
    url(r'^create_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoInListCreate.as_view()),

    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', UserVideoDelete.as_view()),
    url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', UserVideoAbortDelete.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', UserOpenCommentVideo.as_view()),
    url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', UserCloseCommentVideo.as_view()),
    url(r'^on_private/(?P<uuid>[0-9a-f-]+)/$', UserOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<uuid>[0-9a-f-]+)/$', UserOffPrivateVideo.as_view()),
    url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', UserOnVotesVideo.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', UserOffVotesVideo.as_view()),

    url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', VideoUserCommentList.as_view()),
    url(r'^post-comment/$', VideoCommentUserCreate.as_view()),
    url(r'^reply-comment/$', VideoReplyUserCreate.as_view()),
    url(r'^delete_comment/(?P<pk>\d+)/$', VideoCommentUserDelete.as_view()),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', VideoCommentUserAbortDelete.as_view()),
]
