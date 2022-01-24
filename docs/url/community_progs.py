from django.conf.urls import url
from docs.view.community_progs import *


urlpatterns = [
    url(r'^add_list/(?P<pk>\d+)/$', CommunityDocListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', CommunityDocListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', CommunityDocListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', CommunityDocListRecover.as_view()),

    url(r'^create_doc/(?P<pk>\d+)/$', CommunityDocCreate.as_view()),
    url(r'^edit_doc/(?P<doc_pk>\d+)/$', CommunityDocEdit.as_view()),
    url(r'^delete_doc/(?P<doc_pk>\d+)/$', CommunityDocRemove.as_view()),
    url(r'^restore_doc/(?P<doc_pk>\d+)/$', CommunityDocAbortRemove.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', AddDocListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', RemoveDocListFromCommunityCollections.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', CommunityChangeDocPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', CommunityChangeDocListPosition.as_view()),
]
