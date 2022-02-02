from django.conf.urls import url
from managers.view.message import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', MessageCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', MessageCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', MessageRejectedCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', MessageUnverify.as_view()),
    url(r'^send_messages/$', SendManagerMessages.as_view()),
]
