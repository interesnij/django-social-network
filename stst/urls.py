from django.conf.urls import url
from video.views import StatView


urlpatterns = [
    url(r'^$', StatView.as_view(), name='stat'),
]
