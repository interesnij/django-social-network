from goods.view.community import *
from django.urls import re_path


urlpatterns=[
	re_path(r'^detail/(?P<pk>\d+)/(?P<good_pk>\d+)/$', GoodCommunityDetail.as_view(), name="c_good_detail"),
]
