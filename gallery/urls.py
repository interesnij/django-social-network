from django.conf.urls import url, include


urlpatterns=[
	url(r'^user/', include('gallery.urls.user')),
	url(r'^community/', include('gallery.urls.community')),
]
