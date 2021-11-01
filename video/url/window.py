from django.conf.urls import url
from video.view.votes_window import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<pk>\d+)/$', VideoUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<pk>\d+)/$', VideoUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<comment_pk>\d+)/$', VideoUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<comment_pk>\d+)/$', VideoUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<pk>\d+)/$', VideoCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<pk>\d+)/$', VideoCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<comment_pk>\d+)/$', VideoCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<comment_pk>\d+)/$', VideoCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_like/(?P<pk>\d+)/$', AllVideoUserLikeWindow.as_view()),
	url(r'^all_user_dislike/(?P<pk>\d+)/$', AllVideoUserDislikeWindow.as_view()),
    url(r'^all_user_comment_like/(?P<comment_pk>\d+)/$', AllVideoUserCommentLikeWindow.as_view()),
	url(r'^all_user_comment_dislike/(?P<comment_pk>\d+)/$', AllVideoUserCommentDislikeWindow.as_view()),
	url(r'^all_community_like/(?P<pk>\d+)/$', AllVideoCommunityLikeWindow.as_view()),
	url(r'^all_community_dislike/(?P<pk>\d+)/$', AllVideoCommunityDislikeWindow.as_view()),
    url(r'^all_community_comment_like/(?P<comment_pk>\d+)/$', AllVideoCommunityCommentLikeWindow.as_view()),
	url(r'^all_community_comment_dislike/(?P<comment_pk>\d+)/$', AllVideoCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_repost/(?P<pk>\d+)/$', AllVideoUserRepostWindow.as_view()),
	url(r'^all_community_repost/(?P<pk>\d+)/$', AllVideoCommunityRepostWindow.as_view()),
]
