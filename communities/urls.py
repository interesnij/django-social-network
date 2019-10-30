from communities.views import (
                                CommunitiesView,
                                CommunityDetailView,
                                AllCommunities,
                                CommunityCreate,
                                CommunitiesCatsView,
                                CommunityItemView,
                                CommunityListView,
                            )
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', CommunitiesView.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/detail/$', CommunityDetailView.as_view(), name='community_detail'),
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
    url(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    url(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),
    url(r'^item/(?P<pk>\d+)/$', CommunityItemView.as_view(), name='community_item'),
    url(r'^list/(?P<pk>\d+)/$', CommunityListView.as_view(), name="community_item_list"),
]
