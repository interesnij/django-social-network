from django.conf.urls import url
from managers.view.community import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', CommunityAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', CommunityAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', CommunityModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', CommunityModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', CommunityEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', CommunityEditorDelete.as_view()),
    url(r'^add_advertiser/(?P<pk>\d+)/$', CommunityAdvertiserCreate.as_view()),
    url(r'^delete_advertiser/(?P<pk>\d+)/$', CommunityAdvertiserDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', CommunityWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', CommunityWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', CommunityWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', CommunityWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', CommunityWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', CommunityWorkerEditorDelete.as_view()),
    url(r'^add_worker_advertiser/(?P<pk>\d+)/$', CommunityWorkerAdvertiserCreate.as_view()),
    url(r'^delete_worker_advertiser/(?P<pk>\d+)/$', CommunityWorkerAdvertiserDelete.as_view()),

    url(r'^create_suspension/(?P<pk>\d+)/$', CommunitySuspensionCreate.as_view()),
    url(r'^delete_suspension/(?P<pk>\d+)/$', CommunitySuspensionDelete.as_view()),
    url(r'^create_close/(?P<pk>\d+)/$', CommunityCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', CommunityCloseDelete.as_view()),
    url(r'^create_warning_banner/(?P<pk>\d+)/$', CommunityWarningBannerCreate.as_view()),
    url(r'^delete_warning_banner/(?P<pk>\d+)/$', CommunityWarningBannerDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', CommunityRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', CommunityClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', CommunityUnverify.as_view())
]
