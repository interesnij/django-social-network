from django.conf.urls import url, include
from users.views.detail import *
from users.views.lists import AllUsers


urlpatterns = [
    url(r'^detail/', include('users.url.detail')),
    url(r'^settings/', include('users.url.settings')),
    url(r'^load/', include('users.url.load')),
    url(r'^progs/', include('users.url.progs')),
    url(r'^stat/', include('users.url.stat')),

    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^(?P<pk>\d+)/communities/$', UserCommunities.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/staff_communities/$', UserStaffCommunities.as_view(), name='staff_communities'),
    url(r'^(?P<pk>\d+)/mob_staffed/$', UserMobStaffed.as_view(), name='mob_staffed_communities'),
    url(r'^(?P<pk>\d+)/music/$', UserMusic.as_view(), name='user_music'),
    url(r'^(?P<pk>\d+)/video/(?P<uuid>[0-9a-f-]+)/$', UserVideo.as_view(), name='user_video_list'),
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
]
