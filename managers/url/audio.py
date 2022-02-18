from django.conf.urls import url
from managers.view.audio import *


urlpatterns = [
    url(r'^create_rejected/(?P<pk>\d+)/$', AudioRejectedCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', AudioUnverify.as_view()),

    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListAudioRejectedCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListAudioUnverify.as_view()),
]
