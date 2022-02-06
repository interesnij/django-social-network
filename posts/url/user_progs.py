from django.conf.urls import url
from posts.view.user_progs import *


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', PostUserCreate.as_view()),
	url(r'^edit_post/(?P<pk>\d+)/$', PostUserEdit.as_view()),
	url(r'^save_creator_draft_post/(?P<pk>\d+)/$', UserSaveCreatorDraftPost.as_view()),
	url(r'^save_offer_draft_post/(?P<pk>\d+)/$', UserSaveOfferDraftPost.as_view()),
	url(r'^update_votes/(?P<pk>\d+)/$', PostGetVotes.as_view()),

	url(r'^fixed/(?P<pk>\d+)/$', PostUserFixed.as_view()),
    url(r'^unfixed/(?P<pk>\d+)/$', PostUserUnFixed.as_view()),
	url(r'^off_comment/(?P<pk>\d+)/$', PostUserOffComment.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', PostUserOnComment.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', PostUserDelete.as_view()),
	url(r'^restore/(?P<pk>\d+)/$', PostUserRecover.as_view()),
	url(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesPost.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesPost.as_view()),
]
