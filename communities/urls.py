from communities.views import CommunitiesView
from django.conf.urls import url

urlpatterns = [
    url(r'^communities/$', CommunitiesView.as_view(), name='communities')
]
