from communities.views import CommunitiesView, CommunityDetailView, AllCommunities
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', CommunitiesView.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/detail/$', CommunityDetailView.as_view(), name='community_detail'),
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
]
