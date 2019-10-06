from .views import CategoriesEdit, SubCategoriesEdit, Goods
from django.conf.urls import url

urlpatterns=[
	url(r'^$', GoodCategoriesView.as_view(), name="good_categories"),
    url(r'sub/^$', GoodSubCategoriesView.as_view(), name="good_sub_categories"),
    url(r'good/^$', GoodsView.as_view(), name="goods"),
]
