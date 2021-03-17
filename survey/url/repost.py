from survey.view.repost import *
from django.conf.urls import url

urlpatterns = [
    url(r'^u_ucm_survey_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMSurveyWindow.as_view()),
    url(r'^c_ucm_survey_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMSurveyWindow.as_view()),

    url(r'^u_u_survey_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUSurveyRepost.as_view()),
    url(r'^c_u_survey_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUSurveyRepost.as_view()),
    url(r'^u_c_survey_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCSurveyRepost.as_view()),
    url(r'^c_c_survey_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCSurveyRepost.as_view()),
    url(r'^u_m_survey_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMSurveyRepost.as_view()),
    url(r'^c_m_survey_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMSurveyRepost.as_view()),
]
