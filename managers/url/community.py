from django.conf.urls import url
from managers.view.community import *


urlpatterns = [
    url(r'^delete_suspension/(?P<pk>\d+)/$', CommunitySuspensionDelete.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', CommunityCloseDelete.as_view()),
    url(r'^delete_warning_banner/(?P<pk>\d+)/$', CommunityWarningBannerDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', CommunityRejectedCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', CommunityUnverify.as_view())
]
