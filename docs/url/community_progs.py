from django.conf.urls import url
from docs.view.community_progs import *


urlpatterns = [
    url(r'^create_doc/(?P<pk>\d+)/$', CommunityDocCreate.as_view()),
    url(r'^edit_doc/(?P<doc_pk>\d+)/$', CommunityDocEdit.as_view()),
    url(r'^delete_doc/(?P<doc_pk>\d+)/$', CommunityDocRemove.as_view()),
    url(r'^restore_doc/(?P<doc_pk>\d+)/$', CommunityDocAbortRemove.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', AddDocListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', RemoveDocListFromCommunityCollections.as_view()),
]
