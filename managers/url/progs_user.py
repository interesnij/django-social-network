from django.conf.urls import url
from managers.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(UserAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(UserAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(UserModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(UserModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(UserEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(UserEditorDelete.as_view())),
    url(r'^add_advertiser/(?P<pk>\d+)/$', login_required(UserAdvertiserCreate.as_view())),
    url(r'^delete_advertiser/(?P<pk>\d+)/$', login_required(UserAdvertiserDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(UserWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(UserWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(UserWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(UserWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(UserWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(UserWorkerEditorDelete.as_view())),
    url(r'^add_worker_advertiser/(?P<pk>\d+)/$', login_required(UserWorkerAdvertiserCreate.as_view())),
    url(r'^delete_worker_advertiser/(?P<pk>\d+)/$', login_required(UserWorkerAdvertiserDelete.as_view())),

    url(r'^create_suspension/(?P<pk>\d+)/$', login_required(UserSuspensionCreate.as_view())),
    url(r'^delete_suspension/(?P<pk>\d+)/$', login_required(UserSuspensionDelete.as_view())),
    url(r'^create_block/(?P<pk>\d+)/$', login_required(UserBlockCreate.as_view())),
    url(r'^delete_block/(?P<pk>\d+)/$', login_required(UserBlockDelete.as_view())),
    url(r'^create_warning_banner/(?P<pk>\d+)/$', login_required(UserWarningBannerCreate.as_view())),
    url(r'^delete_warning_banner/(?P<pk>\d+)/$', login_required(UserWarningBannerDelete.as_view())),
    url(r'^create_rejected/(?P<pk>\d+)/$', login_required(UserRejectedCreate.as_view())),

    url(r'^suspend_window/(?P<pk>\d+)/$', login_required(UserSuspendWindow.as_view())),
]
