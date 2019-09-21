from frends.views import FrendsListView, ConnectCreate, ConnectDelete2
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<pk>\d+)/$',FrendsListView.as_view(), name="frends"),
    url(r'^add/(?P<pk>\d+)/$', ConnectCreate.as_view(), name="create_connect"),
    url(r'^delete2/(?P<pk>\d+)/$', ConnectDelete2.as_view(), name="delete_connect2"),
]
