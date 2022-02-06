from survey.view.user_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^add/(?P<pk>\d+)/$', SurveyUserCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', SurveyUserEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', SurveyUserDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', SurveyUserRecover.as_view()),
    url(r'^vote/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', UserSurveyVote.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyUserDetail.as_view()),
]
