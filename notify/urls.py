from django.conf.urls import url, include

urlpatterns=[
	url(r'^user/', include('notify.url.user')),
	url(r'^post/', include('notify.url.post')),
	url(r'^good/', include('notify.url.good')),
	url(r'^photo/', include('notify.url.photo')),
]
