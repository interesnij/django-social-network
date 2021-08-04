from django.conf.urls import url
from managers.view.good import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', MessageAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', MessageAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', MessageModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', MessageModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', MessageEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', MessageEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', MessageWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', MessageWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', MessageWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', MessageWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', MessageWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', MessageWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', MessageCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', MessageCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', MessageRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', MessageClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', MessageUnverify.as_view()),
]
