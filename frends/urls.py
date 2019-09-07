from frends.views import FrendsListView
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<pk>\d+)/$',FrendsListView.as_view(), name="frends"),
    ]
