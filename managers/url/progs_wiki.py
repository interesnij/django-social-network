from django.conf.urls import url
from managers.view.wiki import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', WikiAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', WikiAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', WikiModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', WikiModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', WikiEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', WikiEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', WikiWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', WikiWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', WikiWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', WikiWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', WikiWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', WikiWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', WikiCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', WikiCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', WikiRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', WikiClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', WikiUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentWikiCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentWikiCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentWikiRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentWikiClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentWikiUnverify.as_view()),
]
