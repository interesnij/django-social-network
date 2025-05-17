from goods.view.user import *
from django.urls import re_path


urlpatterns=[
	re_path(r'^detail/(?P<pk>\d+)/(?P<good_pk>\d+)/$', GoodUserDetail.as_view(), name="u_good_detail"),
]
