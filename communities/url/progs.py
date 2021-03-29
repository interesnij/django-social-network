from django.conf.urls import url
from communities.views.progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_member/(?P<pk>\d+)/$', CommunityMemberCreate.as_view()),
    url(r'^delete_member/(?P<pk>\d+)/$', CommunityMemberDelete.as_view()),
    url(r'^manager_add_member/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityManageMemberCreate.as_view()),
    url(r'^manager_delete_member/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityManageMemberDelete.as_view()),

    url(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    url(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),

    url(r'^add_admin/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdminCreate.as_view()),
    url(r'^delete_admin/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdminDelete.as_view()),
    url(r'^add_moderator/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityModerCreate.as_view()),
    url(r'^delete_moderator/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityModerDelete.as_view()),
    url(r'^add_editor/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityEditorCreate.as_view()),
    url(r'^delete_editor/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityEditorDelete.as_view()),
    url(r'^add_advertiser/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdvertiserCreate.as_view()),
    url(r'^delete_advertiser/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdvertiserDelete.as_view()),
    url(r'^add_banned/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityBannedCreate.as_view()),
    url(r'^delete_banned/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityBannedDelete.as_view()),
]
