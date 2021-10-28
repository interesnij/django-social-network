from goods.view.community import *
from django.conf.urls import url


urlpatterns=[
	url(r'^detail/(?P<pk>\d+)/(?P<good_pk>\d+)/$', GoodCommunityDetail.as_view(), name="c_good_detail"),
]
