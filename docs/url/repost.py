from docs.view.repost import *
from django.conf.urls import url

urlpatterns = [
# u_ucm_doc - документ пользователя(u) к себе на стену(u), в сообщество (c) или в сообщения(m)
    url(r'^u_ucm_doc_window/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UUCMDocWindow.as_view()),
    url(r'^c_ucm_doc_window/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CUCMDocWindow.as_view()),
    url(r'^u_ucm_list_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUCMDocListWindow.as_view()),
    url(r'^c_ucm_list_window/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUCMDocListWindow.as_view()),

    url(r'^u_u_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UUDocRepost.as_view()),
    url(r'^c_u_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CUDocRepost.as_view()),
    url(r'^u_c_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UCDocRepost.as_view()),
    url(r'^c_c_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CCDocRepost.as_view()),
    url(r'^u_m_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', UMDocRepost.as_view()),
    url(r'^c_m_doc_repost/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CMDocRepost.as_view()),

    url(r'^u_u_doc_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UUDocListRepost.as_view()),
    url(r'^c_u_doc_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CUDocListRepost.as_view()),
    url(r'^u_c_doc_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UCDocListRepost.as_view()),
    url(r'^c_c_doc_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CCDocListRepost.as_view()),
    url(r'^u_m_doc_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UMDocListRepost.as_view()),
    url(r'^c_m_doc_list_repost/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CMDocListRepost.as_view()),
]
