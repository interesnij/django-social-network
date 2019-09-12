from communities.views import CommunitiesView, CommunityDetailView
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', CommunitiesView.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/detail/$', CommunityDetailView.as_view(), name='communiy_detail')
]
