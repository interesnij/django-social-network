from django.conf.urls import url
from managers.view.posts import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(PostAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(PostAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(PostModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(PostModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(PostEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(PostEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(PostWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(PostWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(PostWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(PostWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(PostWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(PostWorkerEditorDelete.as_view())),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCloseCreate.as_view())),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCloseDelete.as_view())),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', login_required(PostRejectedCreate.as_view())),
    url(r'^create_claim/(?P<pk>\d+)/$', login_required(PostClaimCreate.as_view())),
    url(r'^unverify/(?P<post_uuid>[0-9a-f-]+)/(?P<obj_pk>\d+)/$', login_required(PostUnverify.as_view())),

    url(r'^comment_create_close/(?P<pk>\d+)/$', login_required(CommentPostCloseCreate.as_view())),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', login_required(CommentPostCloseDelete.as_view())),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', login_required(CommentPostRejectedCreate.as_view())),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', login_required(CommentPostClaimCreate.as_view())),
    url(r'^comment_unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', login_required(CommentPostUnverify.as_view())),

    url(r'^close_window/(?P<uuid>[0-9a-f-]+)/$', login_required(PostCloseWindow.as_view())),
    url(r'^claim_window/(?P<uuid>[0-9a-f-]+)/$', login_required(PostClaimWindow.as_view())),
    url(r'^close_comment_window/(?P<pk>\d+)/$', login_required(PostCommentCloseWindow.as_view())),
    url(r'^claim_comment_window/(?P<pk>\d+)/$', login_required(PostCommentClaimWindow.as_view())),
]
