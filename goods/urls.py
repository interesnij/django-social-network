from .views import (
					GoodCategoriesView,
					GoodSubCategoriesView,
					UserGoodsView,
					GoodsListView,
					GoodUserCreate,
					GoodsCatsView,
					GoodDetailView,
					)
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/list/$', GoodsListView.as_view(), name="goods_list"),
	url(r'^(?P<pk>\d+)/$', UserGoodsView.as_view(), name="goods"),
    url(r'sub/^$', GoodSubCategoriesView.as_view(), name="good_sub_categories"),
    url(r'cat/^$', GoodCategoriesView.as_view(), name="good_categories"),
	url(r'^add/(?P<pk>\d+)/$', GoodUserCreate.as_view(), name="good_add_user"),
	url(r'^cat/(?P<order>\d+)/$',GoodsCatsView.as_view(), name="good_cats"),
	url(r'^detail/(?P<pk>\d+)/$', GoodDetailView.as_view(), name='good_detail'),
]
