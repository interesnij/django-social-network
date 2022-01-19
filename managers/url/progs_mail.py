from django.conf.urls import url
from managers.view.article import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', MailCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', MailCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', MailRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', MailClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', MailUnverify.as_view()),
]
