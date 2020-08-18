from music.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_music - аудиозапись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_music_window/(?P<pk>\d+)/(?P<track_pk>\d+)/$', UUCMMusicWindow.as_view()),
    url(r'^c_ucm_music_window/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CUCMMusicWindow.as_view()),

    url(r'^u_u_music_repost/(?P<pk>\d+)/(?P<track_pk>\d+)/$', UUMusicRepost.as_view()),
    url(r'^c_u_music_repost/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CUMusicRepost.as_view()),
    url(r'^u_c_music_repost/(?P<pk>\d+)/(?P<track_pk>\d+)/$', UCMusicRepost.as_view()),
    url(r'^c_c_music_repost/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CCMusicRepost.as_view()),
    url(r'^u_m_music_repost/(?P<pk>\d+)/(?P<track_pk>\d+)/$', UMMusicRepost.as_view()),
    url(r'^c_m_music_repost/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CMMusicRepost.as_view()),
]
