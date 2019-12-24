from django.conf.urls import url
from main.view.votes_window import *
from main.models import Item, ItemComment
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityCommentDislikeWindow.as_view())
]
