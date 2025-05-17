from django.urls import re_path, include
from users.views.detail import *
from users.views.lists import *


urlpatterns = [
    re_path(r'^detail/', include('users.url.detail')),
    re_path(r'^settings/', include('users.url.settings')),
    re_path(r'^load/', include('users.url.load')),
    re_path(r'^progs/', include('users.url.progs')),
    re_path(r'^stat/', include('users.url.stat')),

    re_path(r'^(?P<pk>\d+)/communities/$', UserCommunities.as_view(), name='communities'),
    re_path(r'^(?P<pk>\d+)/staff_communities/$', UserStaffCommunities.as_view(), name='staff_communities'),
    re_path(r'^(?P<pk>\d+)/mob_staffed/$', UserMobStaffed.as_view(), name='mob_staffed_communities'),
    re_path(r'^blacklist/$', BlackListUsers.as_view(), name='user_black_list'),
    re_path(r'^all-users/$', AllUsers.as_view(), name='all_users'),

    re_path(r'^(?P<pk>\d+)/docs/$', UserDocs.as_view(), name='user_docs'),
    re_path(r'^(?P<pk>\d+)/doc_list/(?P<uuid>[0-9a-f-]+)/$', UserDocsList.as_view(), name='user_docs_list'),

    re_path(r'^(?P<pk>\d+)/music/$', UserMusic.as_view(), name='user_music'),
    re_path(r'^(?P<pk>\d+)/music_list/(?P<uuid>[0-9a-f-]+)/$', UserMusicList.as_view(), name='user_music_list'),

    re_path(r'^(?P<pk>\d+)/video/$', UserVideo.as_view(), name='user_video'),
    re_path(r'^(?P<pk>\d+)/video_list/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view(), name='user_video_list'),

    re_path(r'^(?P<pk>\d+)/goods/$', UserGoods.as_view(), name='user_goods'),
    re_path(r'^(?P<pk>\d+)/goods_list/(?P<uuid>[0-9a-f-]+)/$', UserGoodsList.as_view(), name='user_good_list'),

    re_path(r'^(?P<pk>\d+)/photos/$', UserGallery.as_view(), name='user_gallery'),
    re_path(r'^(?P<pk>\d+)/photo_list/(?P<uuid>[0-9a-f-]+)/$', UserPhotoList.as_view(), name='user_photo_list'),

    re_path(r'^(?P<pk>\d+)/survey/$', UserSurveys.as_view(), name='user_survey'),
    re_path(r'^(?P<pk>\d+)/survey_list/(?P<uuid>[0-9a-f-]+)/$', UserSurveyList.as_view(), name='user_survey_list'),
]
