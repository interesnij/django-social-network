from django.conf.urls import url
from main.views import MainPageView, ComingView


urlpatterns = [
	url(r'main/$', MainPageView.as_view(), name="main"),
	url(r'^$', ComingView.as_view(), name="coming"),
]
