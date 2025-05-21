from django.urls import re_path
from notify.views import *

urlpatterns=[
	re_path(r'^$', AllNotifyView.as_view(), name='all_notify'),
	re_path(r'^user/$', UNotifyView.as_view(), name='user_notify'),
	re_path(r'^community/(?P<pk>\d+)/$', CNotifyView.as_view(), name='community_notify'),
]
