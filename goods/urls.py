from django.conf.urls import url, include


urlpatterns=[
	url(r'^base/', include('goods.url.base')),
	url(r'^user/', include('goods.url.user')),
	url(r'^community/', include('goods.url.community')),
]
