from django.conf.urls import url
from stst.views import StatView, StatItemView


urlpatterns = [
    url(r'^$', StatView.as_view(), name='stat'),
    url(r'^item/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', StatItemView.as_view(), name='stat_item'),
]
