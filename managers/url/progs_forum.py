from django.conf.urls import url
from managers.view.forum import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', ForumCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', ForumCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', ForumRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', ForumClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', ForumUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentForumCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentForumCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentForumRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentForumClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentForumUnverify.as_view()),
]
