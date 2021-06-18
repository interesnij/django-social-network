from goods.view.community_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentGood.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentGood.as_view()),
    url(r'^hide/(?P<pk>\d+)/$', CommunityHideGood.as_view()),
    url(r'^unhide/(?P<pk>\d+)/$', CommunityUnHideGood.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesGood.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesGood.as_view()),

    url(r'^post-comment/$', login_required(GoodCommentCommunityCreate.as_view())),
    url(r'^reply-comment/$', login_required(GoodReplyCommunityCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentCommunityDelete.as_view())),
	url(r'^restore_comment/(?P<pk>\d+)/$', login_required(GoodCommentCommunityRecover.as_view())),

    url(r'^add/(?P<pk>\d+)/$', GoodCommunityCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/(?P<good_pk>\d+)$', GoodCommunityEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CommunityGoodDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CommunityGoodRecover.as_view()),
    url(r'^add_good_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddGoodInCommunityList.as_view()),
    url(r'^remove_good_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveGoodFromCommunityList.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', GoodListCommunityCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', CommunityGoodListEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', CommunityGoodListDelete.as_view()),
    url(r'^restore_list/(?P<uuid>[0-9a-f-]+)/$', CommunityGoodListRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddGoodListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveGoodListFromCommunityCollections.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', CommunityChangeGoodPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', CommunityChangeGoodListPosition.as_view()),
]
