from django.conf.urls import url
from users.views import AllUsers, ProfileUserView, UserGeneralChange, PostUserView

urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^general/(?P<pk>[0-9]+)/$',
        UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^list/(?P<pk>\d+)/$', PostUserView.as_view(), name="post_user_list"),
]
