from goods.view.community_progs import *
from django.urls import re_path


urlpatterns=[
    re_path(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentGood.as_view()),
    re_path(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentGood.as_view()),
    re_path(r'^hide/(?P<pk>\d+)/$', CommunityHideGood.as_view()),
    re_path(r'^unhide/(?P<pk>\d+)/$', CommunityUnHideGood.as_view()),
    re_path(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesGood.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesGood.as_view()),

    re_path(r'^add/(?P<pk>\d+)/$', GoodCommunityCreate.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/(?P<good_pk>\d+)$', GoodCommunityEdit.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CommunityGoodDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CommunityGoodRecover.as_view()),
]
