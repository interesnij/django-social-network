from django.conf.urls import url
from posts.view.community_progs import *


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', PostCommunityCreate.as_view()),
	url(r'^edit_post/(?P<pk>\d+)/$', PostCommunityEdit.as_view()),
	url(r'^save_creator_draft_post/(?P<pk>\d+)/$', CommunitySaveCreatorDraftPost.as_view()),
	url(r'^save_offer_draft_post/(?P<pk>\d+)/$', CommunitySaveOfferDraftPost.as_view()),
	url(r'^add_offer_post/(?P<pk>\d+)/$', PostOfferCommunityCreate.as_view()),

	url(r'^fixed/(?P<pk>\d+)/$', PostCommunityFixed.as_view()),
    url(r'^unfixed/(?P<pk>\d+)/$', PostCommunityUnFixed.as_view()),
	url(r'^off_comment/(?P<pk>\d+)/$', PostCommunityOffComment.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', PostCommunityOnComment.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', PostCommunityDelete.as_view()),
	url(r'^restore/(?P<pk>\d+)/$', PostCommunityRecover.as_view()),
	url(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesPost.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesPost.as_view()),

	url(r'^add_list/(?P<pk>\d+)/$', CommunityPostsListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', CommunityPostsListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', CommunityPostsListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', CommunityPostsListRecover.as_view()),
	url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddPostsListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemovePostsListFromCommunityCollections.as_view()),

	url(r'^change_position/(?P<pk>\d+)/$', CommunityChangePostPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', CommunityChangePostsListPosition.as_view()),
]
