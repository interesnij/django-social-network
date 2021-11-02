from django.conf.urls import url
from posts.view.user_progs import *


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', PostUserCreate.as_view()),
	url(r'^edit_post/(?P<pk>\d+)/$', PostUserEdit.as_view()),
	url(r'^save_creator_draft_post/(?P<pk>\d+)/$', UserSaveCreatorDraftPost.as_view()),
	url(r'^save_offer_draft_post/(?P<pk>\d+)/$', UserSaveOfferDraftPost.as_view()),
	url(r'^update_votes/(?P<pk>\d+)/$', PostGetVotes.as_view()),

	url(r'^add_comment/$', PostCommentUserCreate.as_view()),
    url(r'^reply_comment/$', PostReplyUserCreate.as_view()),
	url(r'^edit_comment/(?P<pk>\d+)/$', PostUserCommentEdit.as_view()),
	url(r'^delete_comment/(?P<pk>\d+)/$', PostCommentUserDelete.as_view()),
	url(r'^restore_comment/(?P<pk>\d+)/$', PostCommentUserRecover.as_view()),

	url(r'^fixed/(?P<pk>\d+)/$', PostUserFixed.as_view()),
    url(r'^unfixed/(?P<pk>\d+)/$', PostUserUnFixed.as_view()),
	url(r'^off_comment/(?P<pk>\d+)/$', PostUserOffComment.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', PostUserOnComment.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', PostUserDelete.as_view()),
	url(r'^restore/(?P<pk>\d+)/$', PostUserRecover.as_view()),
	url(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesPost.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesPost.as_view()),
	url(r'^add_post_in_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', AddPostInUserList.as_view()),
    url(r'^remove_post_from_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', RemovePostFromUserList.as_view()),

	url(r'^add_list/$', UserPostsListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', UserPostsListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', UserPostsListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', UserPostsListRecover.as_view()),
	url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddPostsListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemovePostsListFromUserCollections.as_view()),

	url(r'^change_position/(?P<pk>\d+)/$', UserChangePostPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangePostsListPosition.as_view()),
]
