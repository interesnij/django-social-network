from django.conf.urls import url
from survey.views import SurveyView


urlpatterns = [
    url(r'^$', SurveyView.as_view(), name='survey'),
]
