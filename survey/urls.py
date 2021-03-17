from django.conf.urls import url, include
from survey.views import SurveyView


urlpatterns = [
    url(r'^$', SurveyView.as_view(), name='survey'),
    url(r'^user_progs/', include('survey.url.user_progs')),
	#url(r'^community_progs/', include('survey.url.community_progs')),
    url(r'^repost/', include('survey.url.repost')),
]
