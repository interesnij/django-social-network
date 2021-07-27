from django.conf.urls import url
from managers.view.survey import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', SurveyAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', SurveyAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', SurveyModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', SurveyModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', SurveyEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', SurveyEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', SurveyWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', SurveyWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', SurveyWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', SurveyWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', SurveyWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', SurveyWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', SurveyCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', SurveyCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', SurveyRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', SurveyClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', SurveyUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListSurveyCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListSurveyCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<uuid>[0-9a-f-]+)/$', ListSurveyRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListSurveyClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListSurveyUnverify.as_view()),
]
