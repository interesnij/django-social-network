from django.conf.urls import url, include
from main.views import *


urlpatterns = [
	url(r'^phone_verify/$', MainPhoneSend.as_view(), name="phone_send"),
	url(r'^services/$', MainServicesView.as_view(), name="main_services"), 

	url(r'^$', PostsListView.as_view(), name="post_list"),

	url(r'^posts/', include('main.url.posts')),
	url(r'^comments/', include('main.url.comments')),
	url(r'^like/', include('main.url.like')),
	url(r'^dislike/', include('main.url.dislike')),
]
