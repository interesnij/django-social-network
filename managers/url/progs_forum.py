from django.conf.urls import url
from managers.view.forum import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', ForumAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', ForumAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', ForumModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', ForumModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', ForumEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', ForumEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', ForumWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', ForumWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', ForumWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', ForumWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', ForumWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', ForumWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', ForumCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', ForumCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', ForumRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', ForumClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', ForumUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentForumCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentForumCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentForumRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentForumClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentForumUnverify.as_view()),
]
