from django.urls import path, include
from follows.views import FollowsView


urlpatterns = [
    url(r'^follows/$', FollowsView.as_view(), name='follows')
]
