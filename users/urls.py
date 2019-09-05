from django.conf.urls import url
from users.views import AllUsers, ProfileUserView

urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='profile-user'),
]
