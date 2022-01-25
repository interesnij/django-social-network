from django.conf.urls import url, include
from main.views import *


urlpatterns = [
	url(r'^phone_verify/$', MainPhoneSend.as_view(), name="phone_send"),
	url(r'^services/$', MainServicesView.as_view(), name="main_services"),

	url(r'^$', NewsListView.as_view(), name="news_list"),
	url(r'^featured/$', FeaturedListView.as_view(), name="featured_list"),
	url(r'^load_custom_link/$', LoadCustomLink.as_view()),
	url(r'^comments/$', ItemCommentList.as_view()),


	#url(r'^posts/', include('main.url.posts')),
	#url(r'^comments/', include('main.url.comments')),
	#url(r'^like/', include('main.url.like')),
	#url(r'^dislike/', include('main.url.dislike')),
]
