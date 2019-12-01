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

	url(r'^like_window/(?P<pk>\d+)/$', LikeWindow.as_view(), name='like_window'),
	url(r'^dislike_window/(?P<pk>\d+)/$', DislikeWindow.as_view(), name='dislike_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', CommentLikeWindow.as_view(), name='comment_like_window'),
	url(r'^comment_dislike_window/(?P<pk>\d+)/$', CommentDislikeWindow.as_view(), name='comment_dislike_window')
]
