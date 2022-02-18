from django.conf.urls import url
from managers.view.user import *


urlpatterns = [
    url(r'^create_rejected/(?P<pk>\d+)/$', UserRejectedCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', UserUnverify.as_view()),
]
