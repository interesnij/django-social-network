from django.conf.urls import url
from posts.view.votes_window import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<pk>\d+)/$', PostUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<pk>\d+)/$', PostUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<comment_pk>\d+)/$', PostUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<comment_pk>\d+)/$', PostUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<pk>\d+)/$', PostCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<pk>\d+)/$', PostCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<comment_pk>\d+)/$', PostCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<comment_pk>\d+)/$', PostCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_like/(?P<pk>\d+)/$', AllPostUserLikeWindow.as_view()),
	url(r'^all_user_dislike/(?P<pk>\d+)/$', AllPostUserDislikeWindow.as_view()),
    url(r'^all_user_comment_like/(?P<comment_pk>\d+)/$', AllPostUserCommentLikeWindow.as_view()),
	url(r'^all_user_comment_dislike/(?P<comment_pk>\d+)/$', AllPostUserCommentDislikeWindow.as_view()),
	url(r'^all_community_like/(?P<pk>\d+)/$', AllPostCommunityLikeWindow.as_view()),
	url(r'^all_community_dislike/(?P<pk>\d+)/$', AllPostCommunityDislikeWindow.as_view()),
    url(r'^all_community_comment_like/(?P<comment_pk>\d+)/$', AllPostCommunityCommentLikeWindow.as_view()),
	url(r'^all_community_comment_dislike/(?P<comment_pk>\d+)/$', AllPostCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_repost/(?P<pk>\d+)/$', AllPostUserRepostWindow.as_view()),
	url(r'^all_community_repost/(?P<pk>\d+)/$', AllPostCommunityRepostWindow.as_view()),
]
