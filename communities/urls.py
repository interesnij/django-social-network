from communities.views import CommunitiesView
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', CommunitiesView.as_view(), name='communities')
]
