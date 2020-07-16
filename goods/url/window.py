from django.conf.urls import url
from goods.view.votes_window import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<uuid>[0-9a-f-]+)/$', GoodUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<uuid>[0-9a-f-]+)/$', GoodUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<comment_pk>\d+)/$', GoodUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<comment_pk>\d+)/$', GoodUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<uuid>[0-9a-f-]+)/$', GoodCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<uuid>[0-9a-f-]+)/$', GoodCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<comment_pk>\d+)/$', GoodCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<comment_pk>\d+)/$', GoodCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_like/(?P<uuid>[0-9a-f-]+)/$', AllGoodUserLikeWindow.as_view()),
	url(r'^all_user_dislike/(?P<uuid>[0-9a-f-]+)/$', AllGoodUserDislikeWindow.as_view()),
    url(r'^all_user_comment_like/(?P<comment_pk>\d+)/$', AllGoodUserCommentLikeWindow.as_view()),
	url(r'^all_user_comment_dislike/(?P<comment_pk>\d+)/$', AllGoodUserCommentDislikeWindow.as_view()),
	url(r'^all_community_like/(?P<uuid>[0-9a-f-]+)/$', AllGoodCommunityLikeWindow.as_view()),
	url(r'^all_community_dislike/(?P<uuid>[0-9a-f-]+)/$', AllGoodCommunityDislikeWindow.as_view()),
    url(r'^all_community_comment_like/(?P<comment_pk>\d+)/$', AllGoodCommunityCommentLikeWindow.as_view()),
	url(r'^all_community_comment_dislike/(?P<comment_pk>\d+)/$', AllGoodCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_repost/(?P<uuid>[0-9a-f-]+)/$', AllGoodUserRepostWindow.as_view()),
	url(r'^all_community_repost/(?P<uuid>[0-9a-f-]+)/$', AllGoodCommunityRepostWindow.as_view()),
]
