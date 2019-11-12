from goods.views import *
from django.conf.urls import url


urlpatterns=[
	url(r'^goods/(?P<pk>\d+)/$', UserGoodsList.as_view(), name="user_goods_list"),
	url(r'^(?P<pk>\d+)/$', UserGoods.as_view(), name="user_goods"),
	url(r'^good/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserGood.as_view(), name='user_good'),
    url(r'sub/^$', GoodSubCategories.as_view(), name="good_sub_categories"),
    url(r'cat/^$', GoodCategories.as_view(), name="good_categories"),
	url(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view(), name="good_add_user"),
	url(r'^cat/(?P<order>\d+)/$',GoodsCats.as_view(), name="good_cats"),
]
