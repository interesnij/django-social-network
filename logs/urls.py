from django.conf.urls import url
from logs.views import LogsView


urlpatterns = [
    url(r'^$', LogsView.as_view(), name='logs'),
]
