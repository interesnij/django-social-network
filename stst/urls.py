from django.conf.urls import url
from stst.views import StatView


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', StatView.as_view(), name='stat'),
]
