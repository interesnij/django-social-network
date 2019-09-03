from django.conf.urls import url
from circles.views import CircleView

urlpatterns = [
    url(r'^circles/$', CircleView.as_view(), name='circles')
]
