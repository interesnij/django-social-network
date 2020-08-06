from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^phone_send/$', MainPhoneSend.as_view(), name="phone_send"),
	url(r'^main/news/$', PostListView.as_view(), name="news_list"),
	url(r'^featured_posts/$', FeaturedPostsView.as_view(), name="featured_post_list"),
]
