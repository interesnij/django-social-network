from django.conf.urls import url
from managers.view.user import *


urlpatterns = [
    url(r'^delete_suspension/(?P<pk>\d+)/$', UserSuspensionDelete.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', UserCloseDelete.as_view()),
    url(r'^delete_warning_banner/(?P<pk>\d+)/$', UserWarningBannerDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', UserRejectedCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', UserUnverify.as_view()),
]
