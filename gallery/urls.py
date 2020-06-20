from django.conf.urls import url, include


urlpatterns=[
	url(r'^user/', include('gallery.url.user')),
	url(r'^user_progs/', include('gallery.url.user_progs')),

	url(r'^community/', include('gallery.url.community')),
	url(r'^load/', include('gallery.url.load')),
	url(r'^votes/', include('gallery.url.votes')),
	url(r'^photo_window/', include('gallery.url.window')),
]
