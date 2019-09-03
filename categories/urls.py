from categories.views import CategoriesView
from django.conf.urls import url

urlpatterns = [
    url(r'^categories/$', CategoriesView.as_view(), name='categories')
]
