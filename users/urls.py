from django.conf.urls import url
from users.views import AllUsers, ProfileUserView, ProfileIdentite

urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^identity/(?P<pk>[0-9]+)/$',
        ProfileIdentite.as_view(), name='profile-identity-form'),
]
