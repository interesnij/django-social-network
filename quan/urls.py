from django.urls import re_path
from quan.views import QuanView, QuanCategoryView


urlpatterns = [
    re_path(r'^(?P<cat_name>[\w\-]+)/$', QuanCategoryView.as_view(), name='quan_categories'),
    re_path(r'^$', QuanView.as_view(), name='quan'),
]
