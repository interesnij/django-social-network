from video.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_video - видеозапись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_video_window/(?P<pk>\d+)/$', UUCMVideoWindow.as_view()),
    url(r'^c_ucm_video_window/(?P<pk>\d+)/$', CUCMVideoWindow.as_view()),
    url(r'^u_ucm_video_list_window/(?P<pk>\d+)/$', UUCMVideoListWindow.as_view()),
    url(r'^c_ucm_video_list_window/(?P<pk>\d+)/$', CUCMVideoListWindow.as_view()),

    url(r'^u_u_video_repost/(?P<pk>\d+)/$', UUVideoRepost.as_view()),
    url(r'^c_u_video_repost/(?P<pk>\d+)/$', CUVideoRepost.as_view()),
    url(r'^u_c_video_repost/(?P<pk>\d+)/$', UCVideoRepost.as_view()),
    url(r'^c_c_video_repost/(?P<pk>\d+)/$', CCVideoRepost.as_view()),
    url(r'^u_m_video_repost/(?P<pk>\d+)/$', UMVideoRepost.as_view()),
    url(r'^c_m_video_repost/(?P<pk>\d+)/$', CMVideoRepost.as_view()),

    url(r'^u_u_video_list_repost/(?P<pk>\d+)/$', UUVideoListRepost.as_view()),
    url(r'^c_u_video_list_repost/(?P<pk>\d+)/$', CUVideoListRepost.as_view()),
    url(r'^u_c_video_list_repost/(?P<pk>\d+)/$', UCVideoListRepost.as_view()),
    url(r'^c_c_video_list_repost/(?P<pk>\d+)/$', CCVideoListRepost.as_view()),
    url(r'^u_m_video_list_repost/(?P<pk>\d+)/$', UMVideoListRepost.as_view()),
    url(r'^c_m_video_list_repost/(?P<pk>\d+)/$', CMVideoListRepost.as_view()),
]
