from django.conf.urls import url
from main.view.votes_window import *
from main.models import Item, ItemComment
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^u_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserLikeWindow.as_view()),
	url(r'^u_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserDislikeWindow.as_view()),
    url(r'^u_comment_like_window/(?P<pk>\d+)/(?P<pk>\d+)/$', ItemUserCommentLikeWindow.as_view()),
	url(r'^u_comment_dislike_window/(?P<pk>\d+)/(?P<pk>\d+)/$', ItemUserCommentDislikeWindow.as_view()),
	url(r'^c_like_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityLikeWindow.as_view()),
	url(r'^c_dislike_window/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityDislikeWindow.as_view()),
    url(r'^c_comment_like_window/(?P<comment_pk>\d+)/(?P<pk>\d+)/$', ItemCommunityCommentLikeWindow.as_view()),
	url(r'^c_comment_dislike_window/(?P<comment_pk>\d+)/(?P<pk>\d+)/$', ItemCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemUserLikeWindow.as_view()),
	url(r'^all_user_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemUserDislikeWindow.as_view()),
    url(r'^all_user_comment_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemUserCommentLikeWindow.as_view()),
	url(r'^all_user_comment_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemUserCommentDislikeWindow.as_view()),
	url(r'^all_community_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemCommunityLikeWindow.as_view()),
	url(r'^all_community_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemCommunityDislikeWindow.as_view()),
    url(r'^all_community_comment_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemCommunityCommentLikeWindow.as_view()),
	url(r'^all_community_comment_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemCommunityCommentDislikeWindow.as_view()),

	url(r'^all_user_repost/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemUserRepostWindow.as_view()),
	url(r'^all_community_repost/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', AllItemCommunityRepostWindow.as_view()),
]
