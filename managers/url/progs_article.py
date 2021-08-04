from django.conf.urls import url
from managers.view.article import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', ArticleAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', ArticleAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', ArticleModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', ArticleModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', ArticleEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', ArticleEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', ArticleWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', ArticleWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', ArticleWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', ArticleWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', ArticleWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', ArticleWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', ArticleCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', ArticleCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', ArticleRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', ArticleClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', ArticleUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListArticleCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListArticleCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListArticleRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListArticleClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListArticleUnverify.as_view()),
]
