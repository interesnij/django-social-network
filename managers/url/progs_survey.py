from django.conf.urls import url
from managers.view.survey import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', SurveyCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', SurveyCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', SurveyRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', SurveyClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', SurveyUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListSurveyCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListSurveyCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListSurveyRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListSurveyClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListSurveyUnverify.as_view()),
]
