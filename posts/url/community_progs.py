from django.conf.urls import url
from posts.view.community_progs import *


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', PostCommunityCreate.as_view()),
	url(r'^edit_post/(?P<uuid>[0-9a-f-]+)/$', PostCommunityEdit.as_view()),
	url(r'^add_offer_post/(?P<pk>\d+)/$', PostOfferCommunityCreate.as_view()),

	url(r'^add_comment/$', PostCommunityCommentCreate.as_view()),
    url(r'^reply_comment/$', PostCommunityReplyCreate.as_view()),
	url(r'^edit_comment/(?P<pk>\d+)/$', PostCommunityCommentEdit.as_view()),
	url(r'^delete_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', PostCommentCommunityDelete.as_view()),
	url(r'^restore_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', PostCommentCommunityRecover.as_view()),
	url(r'^delete_owner_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', PostWallCommentCommunityDelete.as_view()),
	url(r'^restore_owner_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', PostWallCommentCommunityRecover.as_view()),

	url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', PostCommunityFixed.as_view()),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', PostCommunityUnFixed.as_view()),
	url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', PostCommunityOffComment.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', PostCommunityOnComment.as_view()),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', PostCommunityDelete.as_view()),
	url(r'^wall_delete/(?P<uuid>[0-9a-f-]+)/$', PostWallCommunityDelete.as_view()),
	url(r'^restore/(?P<uuid>[0-9a-f-]+)/$', PostCommunityRecover.as_view()),
	url(r'^wall_restore/(?P<uuid>[0-9a-f-]+)/$', PostWallCommunityRecover.as_view()),
	url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesPost.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesPost.as_view()),
	url(r'^add_post_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddPostInCommunityList.as_view()),
    url(r'^remove_post_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovePostFromCommunityList.as_view()),

	url(r'^add_list/(?P<pk>\d+)/$', CommunityPostListCreate.as_view()),
    url(r'^edit_list/(?P<list_pk>\d+)/$', CommunityPostListEdit.as_view()),
    url(r'^delete_list/(?P<list_pk>\d+)/$', CommunityPostListDelete.as_view()),
    url(r'^restore_list/(?P<list_pk>\d+)/$', CommunityPostListRecover.as_view()),
	url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddPostListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemovePostListFromCommunityCollections.as_view()),

	url(r'^change_position/(?P<pk>\d+)/$', CommunityChangePostPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', CommunityChangePostListPosition.as_view()),
]
