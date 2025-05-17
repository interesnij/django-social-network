from django.urls import re_path
from posts.view.community_progs import *


urlpatterns = [
	re_path(r'^add_post/(?P<pk>\d+)/$', PostCommunityCreate.as_view()),
	re_path(r'^edit_post/(?P<pk>\d+)/$', PostCommunityEdit.as_view()),
	re_path(r'^save_creator_draft_post/(?P<pk>\d+)/$', CommunitySaveCreatorDraftPost.as_view()),
	re_path(r'^save_offer_draft_post/(?P<pk>\d+)/$', CommunitySaveOfferDraftPost.as_view()),
	re_path(r'^add_offer_post/(?P<pk>\d+)/$', PostOfferCommunityCreate.as_view()),

	re_path(r'^fixed/(?P<pk>\d+)/$', PostCommunityFixed.as_view()),
    re_path(r'^unfixed/(?P<pk>\d+)/$', PostCommunityUnFixed.as_view()),
	re_path(r'^off_comment/(?P<pk>\d+)/$', PostCommunityOffComment.as_view()),
    re_path(r'^on_comment/(?P<pk>\d+)/$', PostCommunityOnComment.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', PostCommunityDelete.as_view()),
	re_path(r'^restore/(?P<pk>\d+)/$', PostCommunityRecover.as_view()),
	re_path(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesPost.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesPost.as_view()),
]
