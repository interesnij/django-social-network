from django.conf.urls import url
from quan.views import QuanView, QuanCategoryView


urlpatterns = [
    url(r'^(?P<cat_name>[\w\-]+)/$', QuanCategoryView.as_view(), name='quan_categories'),
    url(r'^$', QuanView.as_view(), name='quan'),
]
