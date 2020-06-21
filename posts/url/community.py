from django.conf.urls import url
from posts.view.community import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostCommunityDetail.as_view(), name="community_item_detail"),
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', PostCommunityCommentList.as_view()),
    url(r'^post-comment/$', login_required(PostCommunityCommentCreate.as_view())),
    url(r'^reply-comment/$', login_required(PostCommunityReplyCreate.as_view())),

	url(r'^fixed/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_fixed)),
    url(r'^unfixed/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_unfixed)),
	url(r'^off_comment/(?P<pk>\d+)/$', login_required(community_off_comment)),
    url(r'^on_comment/(?P<pk>\d+)/$', login_required(community_on_comment)),
    url(r'^delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_item_delete)),
	url(r'^abort_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_item_abort_delete)),
	url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesPost.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesPost.as_view())
]
