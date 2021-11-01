from django.conf.urls import url
from gallery.view.votes_window import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<pk>\d+)/$', PhotoUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<pk>\d+)/$', PhotoUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<comment_pk>\d+)/$', PhotoUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<comment_pk>\d+)/$', PhotoUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<pk>\d+)/$', PhotoCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<pk>\d+)/$', PhotoCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<comment_pk>\d+)/$', PhotoCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<comment_pk>\d+)/$', PhotoCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_like/(?P<pk>\d+)/$', AllPhotoUserLikeWindow.as_view()),
	url(r'^all_user_dislike/(?P<pk>\d+)/$', AllPhotoUserDislikeWindow.as_view()),
    url(r'^all_user_comment_like/(?P<comment_pk>\d+)/$', AllPhotoUserCommentLikeWindow.as_view()),
	url(r'^all_user_comment_dislike/(?P<comment_pk>\d+)/$', AllPhotoUserCommentDislikeWindow.as_view()),
	url(r'^all_community_like/(?P<pk>\d+)/$', AllPhotoCommunityLikeWindow.as_view()),
	url(r'^all_community_dislike/(?P<pk>\d+)/$', AllPhotoCommunityDislikeWindow.as_view()),
    url(r'^all_community_comment_like/(?P<comment_pk>\d+)/$', AllPhotoCommunityCommentLikeWindow.as_view()),
	url(r'^all_community_comment_dislike/(?P<comment_pk>\d+)/$', AllPhotoCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_repost/(?P<pk>\d+)/$', AllPhotoUserRepostWindow.as_view()),
	url(r'^all_community_repost/(?P<pk>\d+)/$', AllPhotoCommunityRepostWindow.as_view()),
]
