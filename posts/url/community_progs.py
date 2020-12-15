from django.conf.urls import url
from posts.view.community_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', login_required(PostCommunityCreate.as_view())),
	url(r'^add_offer_post/(?P<pk>\d+)/$', login_required(PostOfferCommunityCreate.as_view())),

	url(r'^post-comment/$', login_required(PostCommunityCommentCreate.as_view())),
    url(r'^reply-comment/$', login_required(PostCommunityReplyCreate.as_view())),
	url(r'^delete_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PostCommentCommunityDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PostCommentCommunityAbortDelete.as_view())),
	url(r'^delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PostWallCommentCommunityDelete.as_view())),
	url(r'^abort_delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PostWallCommentCommunityAbortDelete.as_view())),

	url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityFixed.as_view())),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityUnFixed.as_view())),
	url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityOffComment.as_view())),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityOnComment.as_view())),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityDelete.as_view())),
	url(r'^wall_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(PostWallCommunityDelete.as_view())),
	url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCommunityAbortDelete.as_view())),
	url(r'^wall_abort_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(PostWallCommunityAbortDelete.as_view())),
	url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesPost.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesPost.as_view()),

	url(r'^add_list/(?P<pk>\d+)/$', CommunityPostListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CommunityPostListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CommunityPostListDelete.as_view()),
    url(r'^abort_delete_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CommunityPostListAbortDelete.as_view()),
]
