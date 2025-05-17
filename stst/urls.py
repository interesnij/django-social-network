from django.urls import re_path
from stst.views import StatItemView


urlpatterns = [
    re_path(r'^item/(?P<uuid>[0-9a-f-]+)/$', StatItemView.as_view(), name='stat_item'),
]
