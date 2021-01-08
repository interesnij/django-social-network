from django.conf.urls import url
from docs.view.community import *


urlpatterns = [
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityLoadDoclist.as_view()),
]
