from goods.view.community_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', CommunityGoodDelete.as_view()),
    url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', CommunityGoodAbortDelete.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', CommunityOpenCommentGood.as_view()),
    url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', CommunityCloseCommentGood.as_view()),
    url(r'^hide/(?P<uuid>[0-9a-f-]+)/$', CommunityHideGood.as_view()),
    url(r'^unhide/(?P<uuid>[0-9a-f-]+)/$', CommunityUnHideGood.as_view()),
    url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesGood.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesGood.as_view()),

    url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', GoodCommunityCommentList.as_view()),
    url(r'^post-comment/$', login_required(GoodCommentCommunityCreate.as_view())),
    url(r'^reply-comment/$', login_required(GoodReplyCommunityCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentCommunityDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentCommunityAbortDelete.as_view())),
]
