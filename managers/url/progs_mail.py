from django.conf.urls import url
from managers.view.article import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', MailAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', MailAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', MailModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', MailModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', MailEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', MailEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', MailWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', MailWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', MailWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', MailWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', MailWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', MailWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', MailCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', MailCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', MailRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', MailClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', MailUnverify.as_view()),
]
