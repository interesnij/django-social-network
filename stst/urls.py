from django.conf.urls import url
from stst.views import StatItemView


urlpatterns = [
    url(r'^item/(?P<uuid>[0-9a-f-]+)/$', StatItemView.as_view(), name='stat_item'),
]
