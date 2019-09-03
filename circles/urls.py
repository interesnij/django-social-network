from django.conf.urls import url
from circles.views import CircleView

categories_patterns = [
    url(r'^circles/$', CircleView.as_view(), name='circles')
]
