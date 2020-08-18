from music.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_music - аудиозапись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_music_window/(?P<uuid>[0-9a-f-]+)/$', UUCMMusicWindow.as_view()),
    url(r'^c_ucm_music_window/(?P<uuid>[0-9a-f-]+)/$', CUCMMusicWindow.as_view()),

    url(r'^u_u_music_repost/(?P<uuid>[0-9a-f-]+)/$', UUMusicRepost.as_view()),
    url(r'^c_u_music_repost/(?P<uuid>[0-9a-f-]+)/$', CUMusicRepost.as_view()),
    url(r'^u_c_music_repost/(?P<uuid>[0-9a-f-]+)/$', UCMusicRepost.as_view()),
    url(r'^c_c_music_repost/(?P<uuid>[0-9a-f-]+)/$', CCMusicRepost.as_view()),
    url(r'^u_m_music_repost/(?P<uuid>[0-9a-f-]+)/$', UMMusicRepost.as_view()),
    url(r'^c_m_music_repost/(?P<uuid>[0-9a-f-]+)/$', CMMusicRepost.as_view()),
]
