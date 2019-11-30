from django.conf.urls import url
from main.view.votes import *
from main.models import Item, ItemComment
from common.models import ItemVotes
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(ItemUserLikeCreate.as_view()),name='item_like'),
    url(r'^dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(ItemUserDislikeCreate.as_view()),name='item_dislike'),
    url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/like/$',login_required(ItemCommentUserLikeCreate.as_view()),name='item_comment_like'),
    url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/dislike/$',login_required(ItemCommentUserDislikeCreate.as_view()),name='item_comment_dislike'),

	url(r'^like_window/(?P<pk>\d+)/$', LikeWindow.as_view(), name='like_window'),
	url(r'^dislike_window/(?P<pk>\d+)/$', DislikeWindow.as_view(), name='dislike_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', CommentLikeWindow.as_view(), name='comment_like_window'),
	url(r'^comment_dislike_window/(?P<pk>\d+)/$', CommentDislikeWindow.as_view(), name='comment_dislike_window')
]
