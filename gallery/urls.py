from django.conf.urls import url, include


urlpatterns=[
	url(r'^user/', include('gallery.url.user')),
	url(r'^community/', include('gallery.url.community')),
] 
