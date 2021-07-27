from django.conf.urls import url
from managers.view.audio import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', AudioAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', AudioAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', AudioModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', AudioModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', AudioEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', AudioEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', AudioWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', AudioWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', AudioWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', AudioWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', AudioWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', AudioWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<pk>\d+)/$', AudioCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', AudioCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', AudioRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', AudioClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', AudioUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListAudioCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListAudioCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<uuid>[0-9a-f-]+)/$', ListAudioRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListAudioClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListAudioUnverify.as_view()),
]
