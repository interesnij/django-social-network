from django.urls import re_path
from posts.view.user_progs import *


urlpatterns = [
	re_path(r'^add_post/(?P<pk>\d+)/$', PostUserCreate.as_view()),
	re_path(r'^edit_post/(?P<pk>\d+)/$', PostUserEdit.as_view()),
	re_path(r'^save_creator_draft_post/(?P<pk>\d+)/$', UserSaveCreatorDraftPost.as_view()),
	re_path(r'^save_offer_draft_post/(?P<pk>\d+)/$', UserSaveOfferDraftPost.as_view()),
	re_path(r'^update_votes/(?P<pk>\d+)/$', PostGetVotes.as_view()),

	re_path(r'^fixed/(?P<pk>\d+)/$', PostUserFixed.as_view()),
    re_path(r'^unfixed/(?P<pk>\d+)/$', PostUserUnFixed.as_view()),
	re_path(r'^off_comment/(?P<pk>\d+)/$', PostUserOffComment.as_view()),
    re_path(r'^on_comment/(?P<pk>\d+)/$', PostUserOnComment.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', PostUserDelete.as_view()),
	re_path(r'^restore/(?P<pk>\d+)/$', PostUserRecover.as_view()),
	re_path(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesPost.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesPost.as_view()),
]
