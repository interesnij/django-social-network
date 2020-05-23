from django.conf.urls import url, include
from communities.views.list import AllCommunities, CommunityMembersView, CommunityFriendsView, CommunityCategoryView
from communities.views.details import ItemCommunity, ItemsCommunity, CommunityDetail


urlpatterns = [
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
    url(r'^category/(?P<pk>\d+)/$', CommunityCategoryView.as_view(), name='community_category'),

    url(r'^members/(?P<pk>\d+)/$', CommunityMembersView.as_view(), name='community_members'),
    url(r'^friends/(?P<pk>\d+)/$', CommunityFriendsView.as_view(), name='community_friends'),
    url(r'^(?P<pk>\d+)/$', CommunityDetail.as_view(), name='community_detail'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ItemCommunity.as_view(), name='community_item'),
    url(r'^list/(?P<pk>\d+)/$', ItemsCommunity.as_view(), name="community_item_list"),

    url(r'^manage/', include('communities.url.manage')),
    url(r'^progs/', include('communities.url.progs')),
    url(r'^stat/', include('communities.url.stat')),

]
