from django.urls import re_path
from survey.views import *


urlpatterns = [
    re_path(r'^$', SurveyView.as_view()),
    re_path(r'^load_list/(?P<pk>\d+)/$', LoadSurveyList.as_view(), name="load_survey_list"),

    re_path(r'^add_survey_in_list/(?P<pk>\d+)/$', AddSurveyInList.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$', SurveyEdit.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', SurveyDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/$', SurveyRecover.as_view()),
    re_path(r'^vote/(?P<pk>\d+)/$', SurveyVote.as_view()),
    re_path(r'^unvote/(?P<pk>\d+)/$', SurveyUnVote.as_view()),
    re_path(r'^detail/(?P<pk>\d+)/$', SurveyDetail.as_view()),
    re_path(r'^voters/(?P<pk>\d+)/$', SurveyVoters.as_view()),
]
