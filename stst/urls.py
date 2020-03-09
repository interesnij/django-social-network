from django.conf.urls import url
from stst.views import StatView


urlpatterns = [
    url(r'^$', StatView.as_view(), name='stat'),
]
