from frends.views import FrendsListView, ConnectCreate, ConnectDelete
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<pk>\d+)/$',FrendsListView.as_view(), name="frends"),
    url(r'^add/(?P<pk>\d+)/$', ConnectCreate.as_view(), name="create_connect"),
    url(r'^delete/(?P<pk>\d+)/$', ConnectDelete.as_view(), name="delete_connect"),
]
