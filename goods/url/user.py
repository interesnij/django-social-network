from goods.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^detail/(?P<pk>\d+)/(?P<good_pk>\d+)/$', GoodUserDetail.as_view(), name="u_good_detail"),
]
