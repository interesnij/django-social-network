from django.conf.urls import url, include


urlpatterns=[
	url(r'^user/', include('notifications.url.user')),
	url(r'^item/', include('notifications.url.item')),
	url(r'^good/', include('notifications.url.good')),
	url(r'^photo/', include('notifications.url.photo')),
]
