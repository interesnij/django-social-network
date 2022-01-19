from django.conf.urls import url
from managers.view.wiki import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', WikiCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', WikiCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', WikiRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', WikiClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', WikiUnverify.as_view()),
]
