from django.conf.urls import url
from managers.view.user import (
                                UserAdminCreate,
                                UserAdminDelete,
                                UserModerCreate,
                                UserModerDelete,
                                UserEditorCreate,
                                UserEditorDelete,
                                UserAdvertiserCreate,
                                UserAdvertiserDelete,

                                UserWorkerAdminCreate,
                                UserWorkerAdminDelete,
                                UserWorkerModerCreate,
                                UserWorkerModerDelete,
                                UserWorkerEditorCreate,
                                UserWorkerEditorDelete,
                                UserWorkerAdvertiserCreate,
                                UserWorkerAdvertiserDelete
                            )
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
    url(r'^delete_worker_advertiser/(?P<pk>\d+)/$', login_required(UserWorkerAdvertiserDelete.as_view()))
]
