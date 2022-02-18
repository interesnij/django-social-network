from django.conf.urls import url
from managers.view.forum import *


urlpatterns = [
    url(r'^create_rejected/(?P<pk>\d+)/$', ForumRejectedCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', ForumUnverify.as_view()),

    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentForumRejectedCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentForumUnverify.as_view()),
]
