from django.conf.urls import url, include


urlpatterns=[
	url(r'^user_progs/', include('goods.url.user_progs')),
	url(r'^community_progs/', include('goods.url.community_progs')),
	url(r'^progs/', include('goods.url.progs')),
	url(r'^user/', include('goods.url.user')),
	url(r'^community/', include('goods.url.community')),
	url(r'^votes/', include('goods.url.votes')),
]
