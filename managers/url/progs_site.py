from django.conf.urls import url
from managers.view.good import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', SiteAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', SiteAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', SiteModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', SiteModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', SiteEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', SiteEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', SiteWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', SiteWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', SiteWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', SiteWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', SiteWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', SiteWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', SiteCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', SiteCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', SiteRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', SiteClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', SiteUnverify.as_view()),
]
