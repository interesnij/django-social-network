from django.conf.urls import url
from posts.view.user_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', login_required(PostUserCreate.as_view())),
	url(r'^post_view/(?P<uuid>[0-9a-f-]+)/$', UserPostView.as_view()),
	url(r'^post_market_view/(?P<uuid>[0-9a-f-]+)/$', UserAdPostView.as_view()),
	url(r'^update_votes/(?P<uuid>[0-9a-f-]+)/$', PostGetVotes.as_view()),

	url(r'^post-comment/$', login_required(PostCommentUserCreate.as_view())),
    url(r'^reply-comment/$', login_required(PostReplyUserCreate.as_view())),
	url(r'^delete_comment/(?P<pk>\d+)/$', login_required(PostCommentUserDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(PostCommentUserAbortDelete.as_view())),
	url(r'^delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PostWallCommentUserDelete.as_view())),
	url(r'^abort_delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PostWallCommentUserAbortDelete.as_view())),

	url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', login_required(PostUserFixed.as_view())),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', login_required(PostUserUnFixed.as_view())),
	url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(PostUserOffComment.as_view())),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(PostUserOnComment.as_view())),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', login_required(PostUserDelete.as_view())),
	url(r'^wall_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(PostWallUserDelete.as_view())),
	url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(PostUserAbortDelete.as_view())),
	url(r'^wall_abort_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(PostWallUserAbortDelete.as_view())),
	url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', UserOnVotesPost.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', UserOffVotesPost.as_view()),

	url(r'^add_list/$', UserPostListCreate.as_view()),
    url(r'^edit_list/(?P<list_pk>\d+)/$', UserPostListEdit.as_view()),
    url(r'^delete_list/(?P<list_pk>\d+)/$', UserPostListDelete.as_view()),
    url(r'^abort_delete_list/(?P<list_pk>\d+)/$', UserPostListAbortDelete.as_view()),
]
