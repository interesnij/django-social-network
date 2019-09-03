from django.urls import url, include
from circles.views import CircleView

categories_patterns = [
    url(r'^circles/$', CircleView.as_view(), name='circles')
]
