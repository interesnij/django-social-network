from django.conf.urls import url
from managers.view.photo import (
                                PhotoAdminCreate,
                                PhotoAdminDelete,
                                PhotoModerCreate,
                                PhotoModerDelete,
                                PhotoEditorCreate,
                                PhotoEditorDelete,

                                PhotoWorkerAdminCreate,
                                PhotoWorkerAdminDelete,
                                PhotoWorkerModerCreate,
                                PhotoWorkerModerDelete,
                                PhotoWorkerEditorCreate,
                                PhotoWorkerEditorDelete
                            )
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(PhotoAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(PhotoAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(PhotoModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(PhotoModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(PhotoEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(PhotoEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(PhotoWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(PhotoWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(PhotoWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(PhotoWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(PhotoWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(PhotoWorkerEditorDelete.as_view()))
]
