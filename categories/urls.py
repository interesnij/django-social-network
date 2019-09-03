from django.urls import url, include
from categories.views import CategoriesView

categories_patterns = [
    url(r'^categories/$', CategoriesView.as_view(), name='categories')
]
