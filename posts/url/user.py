from django.conf.urls import url
from posts.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostUserDetail.as_view(), name="user_item_detail"),
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', PostUserCommentList.as_view()),
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
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', UserOffVotesPost.as_view())
]
