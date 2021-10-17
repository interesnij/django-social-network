from posts.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_post - запись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_post_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMPostWindow.as_view()),
    url(r'^c_ucm_post_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMPostWindow.as_view()),
    url(r'^u_ucm_post_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMPostsListWindow.as_view()),
    url(r'^c_ucm_post_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMPostsListWindow.as_view()),

    url(r'^u_u_post_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUPostRepost.as_view()),
    url(r'^c_u_post_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUPostRepost.as_view()),
    url(r'^u_c_post_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCPostRepost.as_view()),
    url(r'^c_c_post_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCPostRepost.as_view()),
    url(r'^u_m_post_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMPostRepost.as_view()),
    url(r'^c_m_post_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMPostRepost.as_view()),

    url(r'^u_u_post_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUPostsListRepost.as_view()),
    url(r'^c_u_post_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUPostsListRepost.as_view()),
    url(r'^u_c_post_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCPostsListRepost.as_view()),
    url(r'^c_c_post_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCPostsListRepost.as_view()),
    url(r'^u_m_post_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMPostsListRepost.as_view()),
    url(r'^c_m_post_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMPostsListRepost.as_view()),
]
