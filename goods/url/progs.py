from goods.view.base import *
from django.conf.urls import url


urlpatterns=[
    url(r'sub/^$', GoodSubCategories.as_view(), name="good_sub_categories"),
    url(r'cat/^$', GoodCategories.as_view(), name="good_categories"),
	url(r'^cat/(?P<order>\d+)/$',GoodsCats.as_view(), name="good_cats"),
]
