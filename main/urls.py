from django.conf.urls import url, include
from main.views import MainPageView, ComingView, NewsListView, MainPhoneVerify


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^phone_verify/$', MainPhoneVerify.as_view(), name="phone_verify"),
	url(r'^main/news/$', NewsListView.as_view(), name="news_list"),

	url(r'^user/', include('main.url.user')),
	url(r'^community/', include('main.url.community')),
	url(r'^votes/', include('main.url.votes')),
	url(r'^window/', include('main.url.window')),
]
