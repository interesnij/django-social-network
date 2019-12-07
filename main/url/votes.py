from django.conf.urls import url
from main.view.votes import *
from main.models import Item, ItemComment
from common.models import ItemVotes
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(ItemUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(ItemUserDislikeCreate.as_view())),
    url(r'^user_comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/like/$',login_required(ItemCommentUserLikeCreate.as_view())),
    url(r'^user_comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/dislike/$',login_required(ItemCommentUserDislikeCreate.as_view())),

	url(r'^community_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(ItemCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(ItemCommunityDislikeCreate.as_view())),
    url(r'^community_comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/like/$',login_required(ItemCommentCommunityLikeCreate.as_view())),
    url(r'^community_comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/dislike/$',login_required(ItemCommentCommunityDislikeCreate.as_view())),

	url(r'^u_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityCommentDislikeWindow.as_view())
]
