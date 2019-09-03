from connections.views import ConnectionsView
from django.conf.urls import url

urlpatterns = [
    url(r'^connections/$', ConnectionsView.as_view(), name='connections')
]
