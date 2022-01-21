from survey.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_video - видеозапись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_survey_window/(?P<pk>\d+)/$', UUCMSurveyWindow.as_view()),
    url(r'^c_ucm_survey_window/(?P<pk>\d+)/$', CUCMSurveyWindow.as_view()),
    url(r'^u_ucm_survey_list_window/(?P<pk>\d+)/$', UUCMSurveyListWindow.as_view()),
    url(r'^c_ucm_survey_list_window/(?P<pk>\d+)/$', CUCMSurveyListWindow.as_view()),

    url(r'^u_u_survey_repost/(?P<pk>\d+)/$', UUSurveyRepost.as_view()),
    url(r'^c_u_survey_repost/(?P<pk>\d+)/$', CUSurveyRepost.as_view()),
    url(r'^u_c_survey_repost/(?P<pk>\d+)/$', UCSurveyRepost.as_view()),
    url(r'^c_c_survey_repost/(?P<pk>\d+)/$', CCSurveyRepost.as_view()),
    url(r'^u_m_survey_repost/(?P<pk>\d+)/$', UMSurveyRepost.as_view()),
    url(r'^c_m_survey_repost/(?P<pk>\d+)/$', CMSurveyRepost.as_view()),

    url(r'^u_u_survey_list_repost/(?P<pk>\d+)/$', UUSurveyListRepost.as_view()),
    url(r'^c_u_survey_list_repost/(?P<pk>\d+)/$', CUSurveyListRepost.as_view()),
    url(r'^u_c_survey_list_repost/(?P<pk>\d+)/$', UCSurveyListRepost.as_view()),
    url(r'^c_c_survey_list_repost/(?P<pk>\d+)/$', CCSurveyListRepost.as_view()),
    url(r'^u_m_survey_list_repost/(?P<pk>\d+)/$', UMSurveyListRepost.as_view()),
    url(r'^c_m_survey_list_repost/(?P<pk>\d+)/$', CMSurveyListRepost.as_view()),
]
