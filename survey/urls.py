from django.conf.urls import url
from survey.views import *


urlpatterns = [
    url(r'^$', SurveyView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadSurveyList.as_view(), name="load_survey_list"),

    url(r'^add_survey_in_list/(?P<pk>\d+)/$', AddSurveyInList.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', SurveyEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', SurveyDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', SurveyRecover.as_view()),
    url(r'^vote/(?P<pk>\d+)/$', SurveyVote.as_view()),
    url(r'^unvote/(?P<pk>\d+)/$', SurveyUnVote.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', SurveyDetail.as_view()),
]
