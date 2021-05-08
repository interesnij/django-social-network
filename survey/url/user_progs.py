from survey.view.user_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^add/$', SurveyUserCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', SurveyUserEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', SurveyUserDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', SurveyUserRecover.as_view()),
    url(r'^vote/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', UserSurveyVote.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyUserDetail.as_view()),

    url(r'^create_list/$', UserSurveyListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserSurveyListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserSurveyListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserSurveyListRecover.as_view()),
    url(r'^add_list_in_collections/(?P<uuid>[0-9a-f-]+)/$', AddSurveyListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<uuid>[0-9a-f-]+)/$', RemoveSurveyListFromUserCollections.as_view()),
]
