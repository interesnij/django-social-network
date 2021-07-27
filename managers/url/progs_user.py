from django.conf.urls import url
from managers.view.user import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', UserAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', UserAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', UserModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', UserModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', UserEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', UserEditorDelete.as_view()),
    url(r'^add_advertiser/(?P<pk>\d+)/$', UserAdvertiserCreate.as_view()),
    url(r'^delete_advertiser/(?P<pk>\d+)/$', UserAdvertiserDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', UserWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', UserWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', UserWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', UserWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', UserWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', UserWorkerEditorDelete.as_view()),
    url(r'^add_worker_advertiser/(?P<pk>\d+)/$', UserWorkerAdvertiserCreate.as_view()),
    url(r'^delete_worker_advertiser/(?P<pk>\d+)/$', UserWorkerAdvertiserDelete.as_view()),

    url(r'^create_suspension/(?P<pk>\d+)/$', UserSuspensionCreate.as_view()),
    url(r'^delete_suspension/(?P<pk>\d+)/$', UserSuspensionDelete.as_view()),
    url(r'^create_close/(?P<pk>\d+)/$', UserCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', UserCloseDelete.as_view()),
    url(r'^create_warning_banner/(?P<pk>\d+)/$', UserWarningBannerCreate.as_view()),
    url(r'^delete_warning_banner/(?P<pk>\d+)/$', UserWarningBannerDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', UserRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', UserClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', UserUnverify.as_view()),
]
