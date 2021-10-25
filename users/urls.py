from django.conf.urls import url, include
from users.views.detail import *
from users.views.lists import *


urlpatterns = [
    url(r'^detail/', include('users.url.detail')),
    url(r'^settings/', include('users.url.settings')),
    url(r'^load/', include('users.url.load')),
    url(r'^progs/', include('users.url.progs')),
    url(r'^stat/', include('users.url.stat')),

    url(r'^(?P<pk>\d+)/communities/$', UserCommunities.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/staff_communities/$', UserStaffCommunities.as_view(), name='staff_communities'),
    url(r'^(?P<pk>\d+)/mob_staffed/$', UserMobStaffed.as_view(), name='mob_staffed_communities'),
    url(r'^blacklist/$', BlackListUsers.as_view(), name='user_black_list'),
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),

    url(r'^(?P<pk>\d+)/docs/$', UserDocs.as_view(), name='user_docs'),
    url(r'^(?P<pk>\d+)/doc_list/(?P<uuid>[0-9a-f-]+)/$', UserDocsList.as_view(), name='user_docs_list'),

    url(r'^(?P<pk>\d+)/music/$', UserMusic.as_view(), name='user_music'),
    url(r'^(?P<pk>\d+)/music_list/(?P<uuid>[0-9a-f-]+)/$', UserMusicList.as_view(), name='user_music_list'),

    url(r'^(?P<pk>\d+)/video/$', UserVideo.as_view(), name='user_video'),
    url(r'^(?P<pk>\d+)/video_list/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view(), name='user_video_list'),

    url(r'^(?P<pk>\d+)/goods/$', UserGoods.as_view(), name='user_goods'),
    url(r'^(?P<pk>\d+)/goods_list/(?P<uuid>[0-9a-f-]+)/$', UserGoodsList.as_view(), name='user_good_list'),

    url(r'^(?P<pk>\d+)/photos/$', UserGallery.as_view(), name='user_gallery'),
    url(r'^(?P<pk>\d+)/photo_list/(?P<uuid>[0-9a-f-]+)/$', UserPhotoList.as_view(), name='user_photo_list'),
]
