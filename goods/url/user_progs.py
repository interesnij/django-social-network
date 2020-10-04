from goods.view.user_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^delete/(?P<pk>\d+)/$', UserGoodDelete.as_view()),
    url(r'^abort_delete/(?P<pk>\d+)/$', UserGoodAbortDelete.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/$', UserOpenCommentGood.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/$', UserCloseCommentGood.as_view()),
    url(r'^hide/(?P<pk>\d+)/$', UserHideGood.as_view()),
    url(r'^unhide/(?P<pk>\d+)/$', UserUnHideGood.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/$', UserOnVotesGood.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/$', UserOffVotesGood.as_view()),

    url(r'^post-comment/$', login_required(GoodCommentUserCreate.as_view())),
    url(r'^reply-comment/$', login_required(GoodReplyUserCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentUserDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(GoodCommentUserAbortDelete.as_view())),

    url(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view()),

    url(r'^add_album/(?P<pk>\d+)/$', GoodAlbumUserCreate.as_view()),
    url(r'^edit_album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserGoodAlbumEdit.as_view()),
    url(r'^delete_album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserGoodAlbumDelete.as_view()),
    url(r'^abort_delete_album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserGoodAlbumAbortDelete.as_view()),

    url(r'^get_album_preview/(?P<pk>\d+)/$', UserGoodAlbumPreview.as_view()),
]
