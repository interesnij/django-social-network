from django.conf.urls import url, include
from goods.views import *


urlpatterns=[
	url(r'^load_list/(?P<uuid>[0-9a-f-]+)/$', LoadGoodList.as_view(), name="load_good_list"),
	url(r'^good/(?P<pk>\d+)/$', GoodDetail.as_view(), name="good_detail"),

	url(r'^user/', include('goods.url.user')),
	url(r'^community/', include('goods.url.community')),

	url(r'^progs/', include('goods.url.progs')),
	url(r'^user_progs/', include('goods.url.user_progs')),
	url(r'^community_progs/', include('goods.url.community_progs')),
]
