from django.urls import re_path, include
from goods.views import *


urlpatterns=[
	re_path(r'^load_list/(?P<pk>\d+)/$', LoadGoodList.as_view(), name="load_good_list"),
	re_path(r'^good/(?P<pk>\d+)/$', GoodDetail.as_view(), name="good_detail"),

	re_path(r'^user/', include('goods.url.user')),
	re_path(r'^community/', include('goods.url.community')),

	re_path(r'^progs/', include('goods.url.progs')),
	re_path(r'^user_progs/', include('goods.url.user_progs')),
	re_path(r'^community_progs/', include('goods.url.community_progs')),
]
