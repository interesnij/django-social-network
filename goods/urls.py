from django.conf.urls import url, include


urlpatterns=[
	url(r'^progs/', include('goods.url.progs')),
	url(r'^user/', include('goods.url.user')),
	url(r'^community/', include('goods.url.community')),
	url(r'^votes/', include('goods.url.votes')),
]
