from django.conf.urls import url
from follows.views import FollowsView


urlpatterns = [
    url(r'^follows/$', FollowsView.as_view(), name='follows')
]
