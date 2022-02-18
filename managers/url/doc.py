from django.conf.urls import url
from managers.view.doc import *


urlpatterns = [
    url(r'^delete_close/(?P<pk>\d+)/$', DocCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', DocRejectedCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', DocUnverify.as_view()),

    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListDocCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListDocRejectedCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListDocUnverify.as_view()),
]
