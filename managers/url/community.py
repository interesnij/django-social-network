from django.conf.urls import url
from managers.view.community import *


urlpatterns = [
    url(r'^create_rejected/(?P<pk>\d+)/$', CommunityRejectedCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', CommunityUnverify.as_view())
]
