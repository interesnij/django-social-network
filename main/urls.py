from django.conf.urls import url, include
from main.views import *


urlpatterns = [
	url(r'^phone_verify/$', MainPhoneSend.as_view(), name="phone_send"),
	url(r'^$', PostsListView.as_view(), name="post_list"),

	url(r'^news/', include('main.url.news')),
	url(r'^featured/', include('main.url.featured')),
	url(r'^comments/', include('main.url.comments')),
	url(r'^like/', include('main.url.like')),
	url(r'^dislike/', include('main.url.dislike')),
]
