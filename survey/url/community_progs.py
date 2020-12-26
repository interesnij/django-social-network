from survey.view.community_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^add/(?P<pk>\d+)/$', SurveyCommunityCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', SurveyCommunityEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', SurveyCommunityDelete.as_view()),
    url(r'^abort_delete/(?P<pk>\d+)/$', SurveyCommunityAbortDelete.as_view()),
    url(r'^vote/(?P<pk>\d+)/$', CommunitySurveyVote.as_view()),
    url(r'^unvote/(?P<pk>\d+)/$', CommunitySurveyUnVote.as_view()),
    url(r'^get_preview/(?P<pk>\d+)/$', CommunitySurveyPreview.as_view()),
]
