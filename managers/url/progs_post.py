from django.conf.urls import url
from managers.view.post import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', PostAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', PostAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', PostModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', PostModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', PostEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', PostEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', PostWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', PostWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', PostWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', PostWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', PostWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', PostWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', PostCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', PostCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', PostRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', PostClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', PostUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListPostCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListPostCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<uuid>[0-9a-f-]+)/$', ListPostRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListPostClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListPostUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentPostCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentPostCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentPostRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentPostClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentPostUnverify.as_view()),
]
