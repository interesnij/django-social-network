from django.conf.urls import url
from managers.view.doc import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', DocAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', DocAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', DocModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', DocModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', DocEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', DocEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', DocWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', DocWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', DocWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', DocWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', DocWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', DocWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<pk>\d+)/$', DocCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', DocCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', DocRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', DocClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', DocUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListDocCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListDocCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<uuid>[0-9a-f-]+)/$', ListDocRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListDocClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListDocUnverify.as_view()),
]
