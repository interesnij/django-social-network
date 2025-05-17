from django.urls import re_path
from search.views import *


urlpatterns = [
    re_path(r'^$', SearchView.as_view(), name='search'),
]
