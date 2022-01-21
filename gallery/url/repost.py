from gallery.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_photo - фотография пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_photo_window/(?P<pk>\d+)/$', UUCMPhotoWindow.as_view()),
    url(r'^c_ucm_photo_window/(?P<pk>\d+)/$', CUCMPhotoWindow.as_view()),
    url(r'^u_ucm_list_window/(?P<pk>\d+)/$', UUCMPhotoListWindow.as_view()),
    url(r'^c_ucm_list_window/(?P<pk>\d+)/$', CUCMPhotoListWindow.as_view()),

    url(r'^u_u_photo_repost/(?P<pk>\d+)/$', UUPhotoRepost.as_view()),
    url(r'^c_u_photo_repost/(?P<pk>\d+)/$', CUPhotoRepost.as_view()),
    url(r'^u_c_photo_repost/(?P<pk>\d+)/$', UCPhotoRepost.as_view()),
    url(r'^c_c_photo_repost/(?P<pk>\d+)/$', CCPhotoRepost.as_view()),
    url(r'^u_m_photo_repost/(?P<pk>\d+)/$', UMPhotoRepost.as_view()),
    url(r'^c_m_photo_repost/(?P<pk>\d+)/$', CMPhotoRepost.as_view()),

    url(r'^u_u_photo_list_repost/(?P<pk>\d+)/$', UUPhotoListRepost.as_view()),
    url(r'^c_u_photo_list_repost/(?P<pk>\d+)/$', CUPhotoListRepost.as_view()),
    url(r'^u_c_photo_list_repost/(?P<pk>\d+)/$', UCPhotoListRepost.as_view()),
    url(r'^c_c_photo_list_repost/(?P<pk>\d+)/$', CCPhotoListRepost.as_view()),
    url(r'^u_m_photo_list_repost/(?P<pk>\d+)/$', UMPhotoListRepost.as_view()),
    url(r'^c_m_photo_list_repost/(?P<pk>\d+)/$', CMPhotoListRepost.as_view()),
]
