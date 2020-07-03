from django.conf.urls import url
from managers.view.community import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(CommunityAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(CommunityAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(CommunityModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(CommunityModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(CommunityEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(CommunityEditorDelete.as_view())),
    url(r'^add_advertiser/(?P<pk>\d+)/$', login_required(CommunityAdvertiserCreate.as_view())),
    url(r'^delete_advertiser/(?P<pk>\d+)/$', login_required(CommunityAdvertiserDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(CommunityWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(CommunityWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(CommunityWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(CommunityWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(CommunityWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(CommunityWorkerEditorDelete.as_view())),
    url(r'^add_worker_advertiser/(?P<pk>\d+)/$', login_required(CommunityWorkerAdvertiserCreate.as_view())),
    url(r'^delete_worker_advertiser/(?P<pk>\d+)/$', login_required(CommunityWorkerAdvertiserDelete.as_view())),

    url(r'^create_suspension/(?P<pk>\d+)/$', login_required(CommunitySuspensionCreate.as_view())),
    url(r'^delete_suspension/(?P<pk>\d+)/$', login_required(CommunitySuspensionDelete.as_view())),
    url(r'^create_block/(?P<pk>\d+)/$', login_required(CommunityBlockCreate.as_view())),
    url(r'^delete_block/(?P<pk>\d+)/$', login_required(CommunityBlockDelete.as_view())),
    url(r'^create_warning_banner/(?P<pk>\d+)/$', login_required(CommunityWarningBannerCreate.as_view())),
    url(r'^delete_warning_banner/(?P<pk>\d+)/$', login_required(CommunityWarningBannerDelete.as_view())),
    url(r'^create_rejected/(?P<pk>\d+)/$', login_required(CommunityRejectedCreate.as_view())),
    url(r'^create_claim/(?P<pk>\d+)/$', login_required(CommunityClaimCreate.as_view())),
    url(r'^unverify/(?P<community_pk>\d+)/(?P<obj_pk>\d+)/$', login_required(CommunityUnverify.as_view())),

    url(r'^suspend_window/(?P<pk>\d+)/$', login_required(CommunitySuspendWindow.as_view())),
    url(r'^block_window/(?P<pk>\d+)/$', login_required(CommunityBlockWindow.as_view())),
    url(r'^warning_banner_window/(?P<pk>\d+)/$', login_required(CommunityWarningBannerdWindow.as_view())),
    url(r'^claim_window/(?P<pk>\d+)/$', login_required(CommunityClaimWindow.as_view())),
]
