from goods.view.user_progs import *
from django.urls import re_path


urlpatterns=[
    re_path(r'^on_comment/(?P<pk>\d+)/$', UserOpenCommentGood.as_view()),
    re_path(r'^off_comment/(?P<pk>\d+)/$', UserCloseCommentGood.as_view()),
    re_path(r'^hide/(?P<pk>\d+)/$', UserHideGood.as_view()),
    re_path(r'^unhide/(?P<pk>\d+)/$', UserUnHideGood.as_view()),
    re_path(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesGood.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesGood.as_view()),

    re_path(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$', GoodUserEdit.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', UserGoodDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/$', UserGoodRecover.as_view()),
]
