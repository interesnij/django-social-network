from django.conf.urls import url, include
from communities.views.list import AllCommunities, CommunityMembersView
from communities.views.details import ItemCommunity, ItemsCommunity, CommunityDetail, CommunityDetailReload
from communities.views.progs import CommunityCreate, CommunitiesCatsView, GygView, CommunityMemberCreate, CommunityMemberDelete


urlpatterns = [
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),

    url(r'^(?P<pk>\d+)/members/$', CommunityMembersView.as_view(), name='community_members'),

    url(r'^(?P<pk>\d+)/$', CommunityDetail.as_view(), name='community_detail'),
    url(r'^reload/(?P<pk>\d+)/$', CommunityDetailReload.as_view(), name='community_detail_reload'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ItemCommunity.as_view(), name='community_item'),
    url(r'^list/(?P<pk>\d+)/$', ItemsCommunity.as_view(), name="community_item_list"),

    url(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    url(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),
    url(r'^gygyg/$', GygView.as_view(), name="community_ggg"),
    url(r'^add_community_member/(?P<pk>\d+)/$', CommunityMemberCreate.as_view(), name="add_community_member"),
    url(r'^delete_community_member/(?P<pk>\d+)/$', CommunityMemberDelete.as_view(), name="delete_community_member"),

    url(r'^manage/', include('communities.url.manage')),

]
