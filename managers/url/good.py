from django.conf.urls import url
from managers.view.goods import (
                                GoodAdminCreate,
                                GoodAdminDelete,
                                GoodModerCreate,
                                GoodModerDelete,
                                GoodEditorCreate,
                                GoodEditorDelete,

                                GoodWorkerAdminCreate,
                                GoodWorkerAdminDelete,
                                GoodWorkerModerCreate,
                                GoodWorkerModerDelete,
                                GoodWorkerEditorCreate,
                                GoodWorkerEditorDelete
                            )
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(GoodAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(GoodAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(GoodModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(GoodModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(GoodEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(GoodEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(GoodWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(GoodWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(GoodWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(GoodWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(GoodWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(GoodWorkerEditorDelete.as_view()))
]
