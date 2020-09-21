from django.conf.urls import url
from goods.view.votes_window import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<good_pk>\d+)/$', GoodUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<good_pk>\d+)/$', GoodUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', GoodUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', GoodUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<good_pk>\d+)/$', GoodCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<good_pk>\d+)/$', GoodCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', GoodCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', GoodCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_like/(?P<good_pk>\d+)/$', AllGoodUserLikeWindow.as_view()),
	url(r'^all_user_dislike/(?P<good_pk>\d+)/$', AllGoodUserDislikeWindow.as_view()),
    url(r'^all_user_comment_like/(?P<comment_pk>\d+)/$', AllGoodUserCommentLikeWindow.as_view()),
	url(r'^all_user_comment_dislike/(?P<comment_pk>\d+)/$', AllGoodUserCommentDislikeWindow.as_view()),
	url(r'^all_community_like/(?P<pk>\d+)/(?P<good_pk>\d+)/$', AllGoodCommunityLikeWindow.as_view()),
	url(r'^all_community_dislike/(?P<pk>\d+)/(?P<good_pk>\d+)/$', AllGoodCommunityDislikeWindow.as_view()),
    url(r'^all_community_comment_like/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', AllGoodCommunityCommentLikeWindow.as_view()),
	url(r'^all_community_comment_dislike/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', AllGoodCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_repost/(?P<good_pk>\d+)/$', AllGoodUserRepostWindow.as_view()),
	url(r'^all_community_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', AllGoodCommunityRepostWindow.as_view()),
]
