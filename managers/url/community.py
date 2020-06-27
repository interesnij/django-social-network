from django.conf.urls import url
from managers.view.community import (
                                CommunityAdminCreate,
                                CommunityAdminDelete,
                                CommunityModerCreate,
                                CommunityModerDelete,
                                CommunityEditorCreate,
                                CommunityEditorDelete,
                                CommunityAdvertiserCreate,
                                CommunityAdvertiserDelete

                                CommunityWorkerAdminCreate,
                                CommunityWorkerAdminDelete,
                                CommunityWorkerModerCreate,
                                CommunityWorkerModerDelete,
                                CommunityWorkerEditorCreate,
                                CommunityWorkerEditorDelete,
                                CommunityWorkerAdvertiserCreate,
                                CommunityWorkerAdvertiserDelete
                            )
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
    url(r'^delete_worker_advertiser/(?P<pk>\d+)/$', login_required(CommunityWorkerAdvertiserDelete.as_view()))
]
