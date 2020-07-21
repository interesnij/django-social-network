from django.conf.urls import url, include
from communities.views.list import *
from communities.views.details import *


urlpatterns = [
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
    url(r'^category/(?P<pk>\d+)/$', CommunityCategoryView.as_view(), name='community_category'),

    url(r'^members/(?P<pk>\d+)/$', CommunityMembersView.as_view(), name='community_members'),
    url(r'^friends/(?P<pk>\d+)/$', CommunityFriendsView.as_view(), name='community_friends'),
    url(r'^(?P<pk>\d+)/$', CommunityDetail.as_view(), name='community_detail'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PostCommunity.as_view(), name='community_item'),
    url(r'^list/(?P<pk>\d+)/$', PostsCommunity.as_view(), name="community_item_list"),
    url(r'^draft/(?P<pk>\d+)/$', PostsDraftCommunity.as_view(), name="community_draft_list"),
    url(r'^(?P<pk>\d+)/music/$', CommunityMusic.as_view(), name='community_music'),
    url(r'^(?P<pk>\d+)/video/$', CommunityVideo.as_view(), name='community_video'),

    url(r'^manage/', include('communities.url.manage')),
    url(r'^progs/', include('communities.url.progs')),
    url(r'^stat/', include('communities.url.stat')),

]
