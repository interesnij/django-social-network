from django.conf.urls import url
from managers.view.posts import (
                                PostAdminCreate,
                                PostAdminDelete,
                                PostModerCreate,
                                PostModerDelete,
                                PostEditorCreate,
                                PostEditorDelete,

                                PostWorkerAdminCreate,
                                PostWorkerAdminDelete,
                                PostWorkerModerCreate,
                                PostWorkerModerDelete,
                                PostWorkerEditorCreate,
                                PostWorkerEditorDelete
                            )
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(PostAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(PostAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(PostModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(PostModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(PostEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(PostEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(PostWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(PostWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(PostWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(PostWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(PostWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(PostWorkerEditorDelete.as_view()))
]
