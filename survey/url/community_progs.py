from survey.view.community_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^add/(?P<pk>\d+)/$', SurveyCommunityCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityRecover.as_view()),
    url(r'^vote/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', CommunitySurveyVote.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyCommunityDetail.as_view()),

    url(r'^create_list/(?P<pk>\d+)/$', CommunitySurveyListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunitySurveyListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunitySurveyListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunitySurveyListRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddSurveyListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovSurveyListFromCommunityCollections.as_view()),
]
