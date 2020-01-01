from django.conf.urls import url
from video.views import AllVideoView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
]
