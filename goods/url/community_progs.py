from goods.view.community_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^on_comment/(?P<pk>\d+)/$', CommunityOpenCommentGood.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', CommunityCloseCommentGood.as_view()),
    url(r'^hide/(?P<pk>\d+)/$', CommunityHideGood.as_view()),
    url(r'^unhide/(?P<pk>\d+)/$', CommunityUnHideGood.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', CommunityOnVotesGood.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', CommunityOffVotesGood.as_view()),

    url(r'^add/(?P<pk>\d+)/$', GoodCommunityCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/(?P<good_pk>\d+)$', GoodCommunityEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CommunityGoodDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CommunityGoodRecover.as_view()),
]
