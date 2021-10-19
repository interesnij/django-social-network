from django.conf.urls import url
from search.views import *


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='search'),
]
