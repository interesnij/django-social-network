from .views import (
					GoodCategoriesView,
					GoodSubCategoriesView,
					UserGoodsView,
					GoodsUserList,
					GoodUserCreate,
					GoodsCatsView,
					UserGoodDetail,
					)
from django.conf.urls import url


urlpatterns=[
	url(r'^user_goods/(?P<pk>\d+)/$', GoodsUserList.as_view(), name="goods_user_list"),
	url(r'^(?P<pk>\d+)/$', UserGoodsView.as_view(), name="goods"),
    url(r'sub/^$', GoodSubCategoriesView.as_view(), name="good_sub_categories"),
    url(r'cat/^$', GoodCategoriesView.as_view(), name="good_categories"),
	url(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view(), name="good_add_user"),
	url(r'^cat/(?P<order>\d+)/$',GoodsCatsView.as_view(), name="good_cats"),
	url(r'^user_good/(?P<pk>\d+)/$', UserGoodDetail.as_view(), name='user_good_detail'),
]
