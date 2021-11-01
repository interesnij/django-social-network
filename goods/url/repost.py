from goods.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_good - товар пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_good_window/(?P<pk>\d+)/(?P<good_pk>\d+)/$', UUCMGoodWindow.as_view()),
    url(r'^c_ucm_good_window/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CUCMGoodWindow.as_view()),

    url(r'^u_ucm_list_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUCMGoodListWindow.as_view()),
    url(r'^c_ucm_list_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUCMGoodListWindow.as_view()),

    url(r'^u_u_good_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', UUGoodRepost.as_view()),
    url(r'^c_u_good_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CUGoodRepost.as_view()),
    url(r'^u_c_good_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', UCGoodRepost.as_view()),
    url(r'^c_c_good_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CCGoodRepost.as_view()),
    url(r'^u_m_good_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', UMGoodRepost.as_view()),
    url(r'^c_m_good_repost/(?P<pk>\d+)/(?P<good_pk>\d+)/$', CMGoodRepost.as_view()),

    url(r'^u_u_good_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUGoodListRepost.as_view()),
    url(r'^c_u_good_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUGoodListRepost.as_view()),
    url(r'^u_c_good_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UCGoodListRepost.as_view()),
    url(r'^c_c_good_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CCGoodListRepost.as_view()),
    url(r'^u_m_good_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UMGoodListRepost.as_view()),
    url(r'^c_m_good_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CMGoodListRepost.as_view()),
]
