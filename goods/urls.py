from .views import (
					GoodCategoriesView,
					GoodSubCategoriesView,
					GoodsListView,
					GoodUserCreate,
					GoodsCatsView,
					GoodDetailView,
					)
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GoodsListView.as_view(), name="goods"),
    url(r'sub/^$', GoodSubCategoriesView.as_view(), name="good_sub_categories"),
    url(r'cat/^$', GoodCategoriesView.as_view(), name="good_categories"),
	url(r'^add/$', GoodUserCreate.as_view(), name="good_add_user"),
	url(r'^cat/(?P<order>\d+)/$',GoodsCatsView.as_view(), name="good_cats"),
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', GoodDetailView.as_view(), name='good_detail'),
]
