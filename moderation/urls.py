from moderation.views import ModerationView
from django.conf.urls import url

urlpatterns = [
    url(r'^moderation/$', ModerationView.as_view(), name='moderation')
]
