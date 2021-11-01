from survey.view.repost import *
from django.conf.urls import url

urlpatterns = [
    url(r'^u_ucm_survey_window/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', UUCMSurveyWindow.as_view()),
    url(r'^c_ucm_survey_window/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', CUCMSurveyWindow.as_view()),

    url(r'^u_u_survey_repost/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', UUSurveyRepost.as_view()),
    url(r'^c_u_survey_repost/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', CUSurveyRepost.as_view()),
    url(r'^u_c_survey_repost/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', UCSurveyRepost.as_view()),
    url(r'^c_c_survey_repost/(?P<pk>\d+)/(?P<survey_pkk>\d+)/$', CCSurveyRepost.as_view()),
    url(r'^u_m_survey_repost/(?P<pk>\d+)/(?P<survey_pkpk>\d+)/$', UMSurveyRepost.as_view()),
    url(r'^c_m_survey_repost/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', CMSurveyRepost.as_view()),
]
