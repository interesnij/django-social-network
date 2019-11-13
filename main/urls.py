from django.conf.urls import url, include
from main.views import MainPageView, ComingView, NewsListView,


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^main/news/$', NewsListView.as_view(), name="news_list"),
	url(r'^user/', include('main.url.user')),
]
