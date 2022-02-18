from django.conf.urls import url
from managers.view.wiki import *


urlpatterns = [
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', WikiCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', WikiRejectedCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', WikiUnverify.as_view()),
]
