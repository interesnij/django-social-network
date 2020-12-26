from django.conf.urls import url, include
from survey.views import SurveyView


urlpatterns = [
    url(r'^$', SurveyView.as_view(), name='survey'),
    url(r'^user_progs/', include('goods.url.user_progs')),
	#url(r'^community_progs/', include('goods.url.community_progs')),
]
