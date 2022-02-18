from django.conf.urls import url
from managers.view.survey import *


urlpatterns = [
    url(r'^create_rejected/(?P<pk>\d+)/$', SurveyRejectedCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', SurveyUnverify.as_view()),

    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListSurveyRejectedCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListSurveyUnverify.as_view()),
]
