from django.conf.urls import url
from dosc.view.user import *


urlpatterns = [
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadDoclist.as_view()),
]
