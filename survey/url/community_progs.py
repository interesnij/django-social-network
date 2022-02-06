from survey.view.community_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^add/(?P<pk>\d+)/$', SurveyCommunityCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityRecover.as_view()),
    url(r'^vote/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', CommunitySurveyVote.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityDetail.as_view()),
]
