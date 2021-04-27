from gallery.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_photo - фотография пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_photo_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMPhotoWindow.as_view()),
    url(r'^c_ucm_photo_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMPhotoWindow.as_view()),
    url(r'^u_ucm_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMPhotoListWindow.as_view()),
    url(r'^c_ucm_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMPhotoListWindow.as_view()),

    url(r'^u_u_photo_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUPhotoRepost.as_view()),
    url(r'^c_u_photo_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUPhotoRepost.as_view()),
    url(r'^u_c_photo_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCPhotoRepost.as_view()),
    url(r'^c_c_photo_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCPhotoRepost.as_view()),
    url(r'^u_m_photo_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMPhotoRepost.as_view()),
    url(r'^c_m_photo_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMPhotoRepost.as_view()),

    url(r'^u_u_photo_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUPhotoListRepost.as_view()),
    url(r'^c_u_photo_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUPhotoListRepost.as_view()),
    url(r'^u_c_photo_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCPhotoListRepost.as_view()),
    url(r'^c_c_photo_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCPhotoListRepost.as_view()),
    url(r'^u_m_photo_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMPhotoListRepost.as_view()),
    url(r'^c_m_photo_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMPhotoListRepost.as_view()),
]
