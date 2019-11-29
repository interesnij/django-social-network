from django.conf.urls import url
from main.view.votes import VotesView, LikeWindow, DislikeWindow, CommentLikeWindow, CommentDislikeWindow
from main.models import Item, Comment
from common.models import LikeDislike
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^like/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.LIKE)),name='item_like'),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.DISLIKE)),name='item_dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',login_required(VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),name='item_comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',login_required(VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),name='item_comment_dislike'),

	url(r'^like_window/(?P<pk>\d+)/$', LikeWindow.as_view(), name='like_window'),
	url(r'^dislike_window/(?P<pk>\d+)/$', DislikeWindow.as_view(), name='dislike_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', CommentLikeWindow.as_view(), name='comment_like_window'),
	url(r'^comment_dislike_window/(?P<pk>\d+)/$', CommentDislikeWindow.as_view(), name='comment_dislike_window'),
]
