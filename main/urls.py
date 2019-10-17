from django.conf.urls import url
from main.views import (
						MainPageView,
						ComingView,
						CommentLikeView,
						CommentDislikeView,
						DislikeView,
						LikeView,
						CommentLikeView,
						CommentDislikeView,
						VotesView,
						get_comment,
						post_comment,
						reply_comment)
from main.models import Item, LikeDislike, Comment
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^like/(?P<item_id>\d+)/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.LIKE)),name='like'),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.DISLIKE)),name='dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',login_required(VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),name='comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',login_required(VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),name='comment_dislike'),
	url(r'^like_window/(?P<pk>\d+)/$', LikeView.as_view(), name='like_window'),
	url(r'^dislike_window/(?P<pk>\d+)/$', DislikeView.as_view(), name='dislike_window'),
	url(r'^comment/$', get_comment, name='get_comment'),
    url(r'^post-comment/$', post_comment, name='post_comment'),
    url(r'^reply-comment/$', reply_comment, name='reply_comment'),
	url(r'^comment_like_window/(?P<pk>\d+)/$', CommentLikeView.as_view(), name='comment_like_window'),
	url(r'^comment_dislike_window/(?P<pk>\d+)/$', CommentDislikeView.as_view(), name='comment_dislike_window'),
]
