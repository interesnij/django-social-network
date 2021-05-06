from django.conf.urls import url
from managers.view.goods import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(GoodAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(GoodAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(GoodModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(GoodModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(GoodEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(GoodEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(GoodWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(GoodWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(GoodWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(GoodWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(GoodWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(GoodWorkerEditorDelete.as_view())),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', login_required(GoodCloseCreate.as_view())),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', login_required(GoodCloseDelete.as_view())),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', login_required(GoodRejectedCreate.as_view())),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', login_required(GoodClaimCreate.as_view())),
    url(r'^unverify/(?P<good_uuid>[0-9a-f-]+)/(?P<obj_pk>\d+)/$', login_required(GoodUnverify.as_view())),

    url(r'^comment_create_close/(?P<pk>\d+)/$', login_required(CommentGoodCloseCreate.as_view())),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', login_required(CommentGoodCloseDelete.as_view())),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', login_required(CommentGoodRejectedCreate.as_view())),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', login_required(CommentGoodClaimCreate.as_view())),
    url(r'^comment_unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', login_required(CommentGoodUnverify.as_view())),

    url(r'^close_window/(?P<uuid>[0-9a-f-]+)/$', login_required(GoodCloseWindow.as_view())),
    url(r'^claim_window/(?P<uuid>[0-9a-f-]+)/$', login_required(GoodClaimWindow.as_view())),
    url(r'^close_comment_window/(?P<pk>\d+)/$', login_required(GoodCommentCloseWindow.as_view())),
    url(r'^claim_comment_window/(?P<pk>\d+)/$', login_required(GoodCommentClaimWindow.as_view())),
]
