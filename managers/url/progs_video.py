from django.conf.urls import url
from managers.view.video import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(VideoAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(VideoAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(VideoModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(VideoModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(VideoEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(VideoEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(VideoWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(VideoWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(VideoWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(VideoWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(VideoWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(VideoWorkerEditorDelete.as_view())),

    url(r'^create_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(VideoDeleteCreate.as_view())),
    url(r'^delete_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(VideoDeleteDelete.as_view())),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', login_required(VideoRejectedCreate.as_view())),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', login_required(VideoClaimCreate.as_view())),
    url(r'^unverify/(?P<video_uuid>[0-9a-f-]+)/(?P<obj_pk>\d+)/$', login_required(VideoUnverify.as_view())),

    url(r'^comment_create_delete/(?P<pk>\d+)/$', login_required(CommentVideoDeleteCreate.as_view())),
    url(r'^comment_delete_delete/(?P<pk>\d+)/$', login_required(CommentVideoDeleteDelete.as_view())),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', login_required(CommentVideoRejectedCreate.as_view())),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', login_required(CommentVideoClaimCreate.as_view())),
    url(r'^comment_unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', login_required(CommentVideoUnverify.as_view())),

    url(r'^delete_window/(?P<uuid>[0-9a-f-]+)/$', login_required(VideoDeleteWindow.as_view())),
    url(r'^claim_window/(?P<uuid>[0-9a-f-]+)/$', login_required(VideoClaimWindow.as_view())),
    url(r'^delete_comment_window/(?P<pk>\d+)/$', login_required(VideoCommentDeleteWindow.as_view())),
    url(r'^claim_comment_window/(?P<pk>\d+)/$', login_required(VideoCommentClaimWindow.as_view())),
]
