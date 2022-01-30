from goods.view.user_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^on_comment/(?P<pk>\d+)/$', UserOpenCommentGood.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', UserCloseCommentGood.as_view()),
    url(r'^hide/(?P<pk>\d+)/$', UserHideGood.as_view()),
    url(r'^unhide/(?P<pk>\d+)/$', UserUnHideGood.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesGood.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesGood.as_view()),

    url(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', GoodUserEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', UserGoodDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', UserGoodRecover.as_view()),

    url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddGoodListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemoveGoodListFromUserCollections.as_view()),
    url(r'^change_position/(?P<pk>\d+)/$', UserChangeGoodPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangeGoodListPosition.as_view()),
]
