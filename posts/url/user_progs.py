from django.conf.urls import url
from posts.view.user_progs import *


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', PostUserCreate.as_view()),
	url(r'^edit_post/(?P<uuid>[0-9a-f-]+)/$', PostUserEdit.as_view()),
	url(r'^save_creator_draft_post/(?P<pk>\d+)/$', UserSaveCreatorDraftPost.as_view()),
	url(r'^save_offer_draft_post/(?P<pk>\d+)/$', UserSaveOfferDraftPost.as_view()),
	url(r'^post_view/(?P<uuid>[0-9a-f-]+)/$', UserPostView.as_view()),
	url(r'^post_market_view/(?P<uuid>[0-9a-f-]+)/$', UserAdPostView.as_view()),
	url(r'^update_votes/(?P<uuid>[0-9a-f-]+)/$', PostGetVotes.as_view()),

	url(r'^add_comment/$', PostCommentUserCreate.as_view()),
    url(r'^reply_comment/$', PostReplyUserCreate.as_view()),
	url(r'^edit_comment/(?P<pk>\d+)/$', PostUserCommentEdit.as_view()),
	url(r'^delete_comment/(?P<pk>\d+)/$', PostCommentUserDelete.as_view()),
	url(r'^restore_comment/(?P<pk>\d+)/$', PostCommentUserRecover.as_view()),
	url(r'^delete_owner_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', PostWallCommentUserDelete.as_view()),
	url(r'^restore_owner_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', PostWallCommentUserRecover.as_view()),

	url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', PostUserFixed.as_view()),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', PostUserUnFixed.as_view()),
	url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', PostUserOffComment.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', PostUserOnComment.as_view()),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', PostUserDelete.as_view()),
	url(r'^wall_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PostWallUserDelete.as_view()),
	url(r'^restore/(?P<uuid>[0-9a-f-]+)/$', PostUserRecover.as_view()),
	url(r'^wall_restore/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PostWallUserRecover.as_view()),
	url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', UserOnVotesPost.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', UserOffVotesPost.as_view()),
	url(r'^add_post_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddPostInUserList.as_view()),
    url(r'^remove_post_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovePostFromUserList.as_view()),

	url(r'^add_list/$', UserPostsListCreate.as_view()),
    url(r'^edit_list/(?P<list_pk>\d+)/$', UserPostsListEdit.as_view()),
    url(r'^delete_list/(?P<list_pk>\d+)/$', UserPostsListDelete.as_view()),
    url(r'^restore_list/(?P<list_pk>\d+)/$', UserPostsListRecover.as_view()),
	url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddPostsListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemovePostsListFromUserCollections.as_view()),

	url(r'^change_position/(?P<pk>\d+)/$', UserChangePostPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangePostsListPosition.as_view()),
]
