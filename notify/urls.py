from django.conf.urls import url, include
from notify.views import MainNotifyView

urlpatterns=[
	url(r'^$', AllNotifyView.as_view(), name='all_notify'),
	url(r'^user/$', UserNotifyView.as_view(), name='user_notify'),
	url(r'^community/(?P<pk>\d+)/$', CommunityNotifyView.as_view(), name='community_notify'),

	url(r'^user/', include('notify.url.user')),
	url(r'^post/', include('notify.url.post')),
	url(r'^good/', include('notify.url.good')),
	url(r'^photo/', include('notify.url.photo')),
]
