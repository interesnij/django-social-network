from categories.views import CategoriesView
from django.conf.urls import url

categories_patterns = [
    url(r'^categories/$', CategoriesView.as_view(), name='categories')
]
