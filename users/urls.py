from django.conf.urls import url
from users.views.settings import UserGeneralChange, UserAboutChange, SettingsNotifyView, SettingsPrivateView, UserAvatarChange, UserDesign
from users.views.progs import fixed, unfixed, item_delete
from users.views.load import ProfileStatReload, ProfileButtonReload, AvatarReload, ProfileReload
from users.views.detail import AllUsers, ProfileUserView, ItemListView, UserItemView


urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserItemView.as_view(), name='user_item'),
    url(r'^list/(?P<pk>\d+)/$', ItemListView.as_view(), name="user_item_list"),

    url(r'^general/(?P<pk>[0-9]+)/$',
        UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^about/(?P<pk>[0-9]+)/$',
        UserAboutChange.as_view(), name='user_about_form'),
    url(r'^design/(?P<pk>\d+)/$', UserDesign.as_view(), name='user_design'),

    url(r'^settings_notify/(?P<pk>[0-9]+)/$',
        SettingsNotifyView.as_view(), name='user_settings_notify'),
    url(r'^settings_private/(?P<pk>[0-9]+)/$',
        SettingsPrivateView.as_view(), name='user_settings_private'),

    url(r'^avatar/(?P<pk>[0-9]+)/$',
        UserAvatarChange.as_view(), name='user_avatar_form'),

    url(r'^profile_button/(?P<pk>\d+)/$', ProfileButtonReload.as_view(), name='profile_button_reload'),
    url(r'^profile_stat/(?P<pk>\d+)/$', ProfileStatReload.as_view(), name='profile_stat_reload'),
    url(r'^avatar-reload/$', AvatarReload.as_view(), name='avatar_reload'),
    url(r'^(?P<pk>\d+)/profile_reload/$', ProfileReload.as_view(), name='profile_reload'),

    url(r'^fixed/(?P<item_id>\d+)/$', fixed, name='fixed'),
    url(r'^unfixed/(?P<item_id>\d+)/$', unfixed, name='unfixed'),
    url(r'^delete/(?P<item_id>\d+)/$', item_delete, name='item_delete'),


]
