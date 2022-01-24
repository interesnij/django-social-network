from posts.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_post - запись пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_post_window/(?P<pk>\d+)/$', UUCMPostWindow.as_view()),
    url(r'^c_ucm_post_window/(?P<pk>\d+)/$', CUCMPostWindow.as_view()),
    url(r'^u_ucm_post_list_window/(?P<pk>\d+)/$', UUCMPostsListWindow.as_view()),
    url(r'^c_ucm_post_list_window/(?P<pk>\d+)/$', CUCMPostsListWindow.as_view()),

    url(r'^u_u_post_repost/(?P<pk>\d+)/$', UUPostRepost.as_view()),
    url(r'^c_u_post_repost/(?P<pk>\d+)/$', CUPostRepost.as_view()),
    url(r'^u_c_post_repost/(?P<pk>\d+)/$', UCPostRepost.as_view()),
    url(r'^c_c_post_repost/(?P<pk>\d+)/$', CCPostRepost.as_view()),
    url(r'^u_m_post_repost/(?P<pk>\d+)/$', UMPostRepost.as_view()),
    url(r'^c_m_post_repost/(?P<pk>\d+)/$', CMPostRepost.as_view()),

    url(r'^u_u_post_list_repost/(?P<pk>\d+)/$', UUPostListRepost.as_view()),
    url(r'^c_u_post_list_repost/(?P<pk>\d+)/$', CUPostListRepost.as_view()),
    url(r'^u_c_post_list_repost/(?P<pk>\d+)/$', UCPostListRepost.as_view()),
    url(r'^c_c_post_list_repost/(?P<pk>\d+)/$', CCPostListRepost.as_view()),
    url(r'^u_m_post_list_repost/(?P<pk>\d+)/$', UMPostListRepost.as_view()),
    url(r'^c_m_post_list_repost/(?P<pk>\d+)/$', CMPostListRepost.as_view()),

    url(r'^u_u_post_copy/(?P<pk>\d+)/$', UUPostCopy.as_view()),
    url(r'^c_u_post_copy/(?P<pk>\d+)/$', CUPostCopy.as_view()),
    url(r'^u_c_post_copy/(?P<pk>\d+)/$', UCPostCopy.as_view()),
    url(r'^c_c_post_copy/(?P<pk>\d+)/$', CCPostCopy.as_view()),
]
