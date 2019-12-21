from django.conf.urls import url, include
from users.views.detail import ProfileUserView, AllUsers
from users.views.lists import CommunitiesView, AllCommonUsers


urlpatterns = [
    url(r'^detail/', include('users.url.detail')),
    url(r'^settings/', include('users.url.settings')),
    url(r'^load/', include('users.url.load')),
    url(r'^progs/', include('users.url.progs')),


    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^(?P<pk>\d+)/communities/$', CommunitiesView.as_view(), name='communities'),
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/common-users/$', AllCommonUsers.as_view(), name='all_common_users'),
]
