from goods.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^good/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserGood.as_view(), name='user_good'),
	url(r'^detail/(?P<pk>\d+)/(?P<good_pk>\d+)/$', GoodUserDetail.as_view(), name="u_good_detail"),
]
