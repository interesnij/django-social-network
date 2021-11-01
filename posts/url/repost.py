from posts.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_post - запись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_post_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUCMPostWindow.as_view()),
    url(r'^c_ucm_post_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUCMPostWindow.as_view()),
    url(r'^u_ucm_post_list_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUCMPostsListWindow.as_view()),
    url(r'^c_ucm_post_list_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUCMPostsListWindow.as_view()),

    url(r'^u_u_post_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUPostRepost.as_view()),
    url(r'^c_u_post_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUPostRepost.as_view()),
    url(r'^u_c_post_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UCPostRepost.as_view()),
    url(r'^c_c_post_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CCPostRepost.as_view()),
    url(r'^u_m_post_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UMPostRepost.as_view()),
    url(r'^c_m_post_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CMPostRepost.as_view()),

    url(r'^u_u_post_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUPostsListRepost.as_view()),
    url(r'^c_u_post_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUPostsListRepost.as_view()),
    url(r'^u_c_post_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UCPostsListRepost.as_view()),
    url(r'^c_c_post_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CCPostsListRepost.as_view()),
    url(r'^u_m_post_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UMPostsListRepost.as_view()),
    url(r'^c_m_post_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CMPostsListRepost.as_view()),
]
