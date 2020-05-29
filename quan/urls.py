from django.conf.urls import url
from quan.views import QuanCategoryView


urlpatterns = [
    url(r'^(?P<cat_name>[\w\-]+)/$', QuanCategoryView.as_view(), name='quan_categories'),
]
