from django.conf.urls import url
from users.views import AllUsers, ProfileUserView, UserGeneralChange, UserAboutChange, UserDesign, PostUserView, UserAvatarChange
from users.views import get_thread, post_comment, update_interactions
from users.views import ProfileButtonReload

urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^general/(?P<pk>[0-9]+)/$',
        UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^list/(?P<pk>\d+)/$', PostUserView.as_view(), name="post_user_list"),
    url(r'^about/(?P<pk>[0-9]+)/$',
        UserAboutChange.as_view(), name='user_about_form'),
    url(r'^design/(?P<pk>\d+)/$', UserDesign.as_view(), name='user_design'),
    url(r'^get-thread/$', get_thread, name='get_thread'),
    url(r'^post-comment/$', post_comment, name='post_comments'),
    url(r'^update-interactions/$', update_interactions, name='update_interactions'),
    url(r'^avatar/(?P<pk>[0-9]+)/$',
        UserAvatarChange.as_view(), name='user_avatar_form'),
    url(r'^profile_button/(?P<pk>[0-9]+)/$', ProfileButtonReload.as_view(), name='profile_btton_reload'),
]
