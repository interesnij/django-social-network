from survey.view.user_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^add/(?P<pk>\d+)/$', SurveyUserCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', SurveyUserEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', SurveyUserDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/$', SurveyUserRecover.as_view()),
    url(r'^vote/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', UserSurveyVote.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<survey_pk>\d+)/$', SurveyUserDetail.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', UserSurveyListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', UserSurveyListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', UserSurveyListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', UserSurveyListRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddSurveyListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemoveSurveyListFromUserCollections.as_view()),
    url(r'^change_position/(?P<pk>\d+)/$', UserChangeSurveyPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangeSurveyListPosition.as_view()),
]
