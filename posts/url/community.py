from django.conf.urls import url
from posts.view.community import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostCommunityDetail.as_view(), name="community_item_detail"),
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', PostCommunityCommentList.as_view()),
    url(r'^post-comment/$', login_required(PostCommunityCommentCreate.as_view())),
    url(r'^reply-comment/$', login_required(PostCommunityReplyCreate.as_view())),
	url(r'^delete_comment/(?P<pk>\d+)/$', login_required(PostCommentCommunityDelete.as_view())), 
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(PostCommentCommunityAbortDelete.as_view())),

	url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityFixed.as_view())),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityUnFixed.as_view())),
	url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityOffComment.as_view())),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityOnComment.as_view())),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityAbortDelete.as_view())),
	url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityAbortDelete.as_view())),
	url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesPost.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesPost.as_view())
]
