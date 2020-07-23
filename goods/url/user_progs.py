from goods.view.user_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', UserGoodDelete.as_view()),
    url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', UserGoodAbortDelete.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', UserOpenCommentGood.as_view()),
    url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', UserCloseCommentGood.as_view()),
    url(r'^hide/(?P<uuid>[0-9a-f-]+)/$', UserHideGood.as_view()),
    url(r'^unhide/(?P<uuid>[0-9a-f-]+)/$', UserUnHideGood.as_view()),
    url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', UserOnVotesGood.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', UserOffVotesGood.as_view()),

    url(r'^post-comment/$', login_required(GoodCommentUserCreate.as_view())),
    url(r'^reply-comment/$', login_required(GoodReplyUserCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentUserDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentUserAbortDelete.as_view())),

    url(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view()),
	url(r'^add_attach/(?P<pk>\d+)/$', GoodUserCreateAttach.as_view())
]
