from django.conf.urls import url
from managers.view.audio import *


urlpatterns = [
    url(r'^create_close/(?P<pk>\d+)/$', AudioCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', AudioCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', AudioRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', AudioClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', AudioUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListAudioCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListAudioCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListAudioRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListAudioClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListAudioUnverify.as_view()),
]
