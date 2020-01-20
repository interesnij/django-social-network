from django.conf.urls import url
from communities.views.progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    url(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),
    url(r'^gygyg/$', GygView.as_view(), name="community_ggg"),
    url(r'^add_member/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityMemberCreate.as_view()),
    url(r'^delete_member/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityMemberDelete.as_view()),

    url(r'^add_admin/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityModerDelete.as_view()),
]
