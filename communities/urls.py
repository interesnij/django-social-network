from django.conf.urls import url
from communities.views.list import AllCommunities, CommunitiesView, CommunityMembersView
from communities.views.details import CommunityItemView, CommunityListView, CommunityDetailView, CommunityDetailReload
from communities.views.progs import CommunityCreate, CommunitiesCatsView, GygView, CommunityMemberCreate, CommunityMemberDelete
from communities.views.manage import CommunityGeneralChange



urlpatterns = [
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
    url(r'^user/(?P<pk>\d+)/$', CommunitiesView.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/members/$', CommunityMembersView.as_view(), name='community_members'),

    url(r'^(?P<pk>\d+)/$', CommunityDetailView.as_view(), name='community_detail'),
    url(r'^reload/(?P<pk>\d+)/$', CommunityDetailReload.as_view(), name='community_detail_reload'),
    url(r'^item/(?P<pk>\d+)/$', CommunityItemView.as_view(), name='community_item'),
    url(r'^list/(?P<pk>\d+)/$', CommunityListView.as_view(), name="community_item_list"),

    url(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    url(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),
    url(r'^gygyg/$', GygView.as_view(), name="community_ggg"),
    url(r'^add_community_member/(?P<pk>\d+)/$', CommunityMemberCreate.as_view(), name="add_community_member"),
    url(r'^delete_community_member/(?P<pk>\d+)/$', CommunityMemberDelete.as_view(), name="delete_community_member"),

    url(r'^general/(?P<pk>[0-9]+)/$', CommunityGeneralChange.as_view(), name='commnity_general_form'),


]
