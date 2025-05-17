from goods.view.progs import *
from django.urls import re_path


urlpatterns=[
    re_path(r'sub/^$', GoodSubCategories.as_view(), name="good_sub_categories"),
    re_path(r'cat/^$', GoodCategories.as_view(), name="good_categories"),
	re_path(r'^cat/(?P<order>\d+)/$',GoodsCats.as_view(), name="good_cats"),
]
