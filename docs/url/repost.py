from music.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_doc - документ пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_doc_window/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UUCMDocWindow.as_view()),
    url(r'^c_ucm_doc_window/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CUCMDocWindow.as_view()),
    url(r'^u_ucm_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUCMDocListWindow.as_view()),
    url(r'^c_ucm_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUCMDocListWindow.as_view()),

    url(r'^u_u_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UUDocRepost.as_view()),
    url(r'^c_u_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CUDocRepost.as_view()),
    url(r'^u_c_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UCDocRepost.as_view()),
    url(r'^c_c_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CCDocRepost.as_view()),
    url(r'^u_m_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UMDocRepost.as_view()),
    url(r'^c_m_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CMDocRepost.as_view()),

    url(r'^u_u_doc_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UUDocListRepost.as_view()),
    url(r'^c_u_doc_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CUDocListRepost.as_view()),
    url(r'^u_c_doc_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UCDocListRepost.as_view()),
    url(r'^c_c_doc_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CCDocListRepost.as_view()),
    url(r'^u_m_doc_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UMDocListRepost.as_view()),
    url(r'^c_m_doc_list_repost/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CMDocListRepost.as_view()),
]
