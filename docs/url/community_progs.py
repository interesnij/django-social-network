from django.conf.urls import url
from docs.view.community_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^create_list_window/(?P<pk>\d+)/$', CommunityCreateDoclistWindow.as_view()),
    url(r'^create_doc_window/(?P<pk>\d+)/$', CommunityCreateDocWindow.as_view()),

    url(r'^create_list/(?P<pk>\d+)/$', CommunityDoclistCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDoclistEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDoclistDelete.as_view()),
    url(r'^abort_delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDoclistAbortDelete.as_view()),
    url(r'^add_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDoclistAdd.as_view()),
    url(r'^remove_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDoclistRemove.as_view()),

    url(r'^create_doc/(?P<pk>\d+)/$', CommunityDocCreate.as_view()),

    url(r'^c_add_doc/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityDocAdd.as_view())),
    url(r'^c_remove_doc/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', login_required(CommunityDocRemove.as_view())),
    url(r'^c_add_doc_in_list/(?P<doc_pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityDocListAdd.as_view())),
    url(r'^c_remove_doc_in_list/(?P<doc_pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityDocListRemove.as_view())),
]
