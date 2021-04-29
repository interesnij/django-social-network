from django.conf.urls import url
from docs.view.community_progs import *


urlpatterns = [
    url(r'^create_list/(?P<pk>\d+)/$', CommunityDocListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDocListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDocListDelete.as_view()),
    url(r'^abort_delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDocListAbortDelete.as_view()),

    url(r'^create_doc/(?P<pk>\d+)/$', CommunityDocCreate.as_view()),
    url(r'^edit_doc/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CommunityDocEdit.as_view()),
    url(r'^remove_doc/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CommunityDocRemove.as_view()),
    url(r'^abort_remove_doc/(?P<pk>\d+)/(?P<doc_pk>\d+)/$', CommunityDocAbortRemove.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddDocListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveDocListFromCommunityCollections.as_view()),
]
