from django.conf.urls import url
from users.views import AllUsers, ProfileUserView, UserGeneralChange, UserAboutChange, UserDesign, PostUserView

urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^general/(?P<pk>[0-9]+)/$',
        UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^list/(?P<pk>\d+)/$', PostUserView.as_view(), name="post_user_list"),
    url(r'^about/(?P<pk>[0-9]+)/$',
        UserAboutChange.as_view(), name='user_about_form'),
    url(r'^(?P<pk>\d+)/$', UserDesign.as_view(), name='user_design'),
]
