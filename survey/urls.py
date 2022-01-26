from django.conf.urls import url, include
from survey.views import SurveyView, LoadSurveyList


urlpatterns = [
    url(r'^$', SurveyView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadSurveyList.as_view(), name="load_survey_list"),

    url(r'^user_progs/', include('survey.url.user_progs')),
	#url(r'^community_progs/', include('survey.url.community_progs')),
]
