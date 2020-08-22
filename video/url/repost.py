from video.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_video - видеозапись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_video_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMVideoWindow.as_view()),
    url(r'^c_ucm_video_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMVideoWindow.as_view()),
    url(r'^u_ucm_video_album_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMVideoAlbumWindow.as_view()),
    url(r'^c_ucm_video_album_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMVideoAlbumWindow.as_view()),

    url(r'^u_u_video_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUVideoRepost.as_view()),
    url(r'^c_u_video_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUVideoRepost.as_view()),
    url(r'^u_c_video_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCVideoRepost.as_view()),
    url(r'^c_c_video_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCVideoRepost.as_view()),
    url(r'^u_m_video_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMVideoRepost.as_view()),
    url(r'^c_m_video_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMVideoRepost.as_view()),

    url(r'^u_u_video_album_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUVideoAlbumRepost.as_view()),
    url(r'^c_u_video_album_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUVideoAlbumRepost.as_view()),
    url(r'^u_c_video_album_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCVideoAlbumRepost.as_view()),
    url(r'^c_c_video_album_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCVideoAlbumRepost.as_view()),
    url(r'^u_m_video_album_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMVideoAlbumRepost.as_view()),
    url(r'^c_m_video_album_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMVideoAlbumRepost.as_view()),
]
