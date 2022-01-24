from django.conf.urls import url
from docs.view.user_progs import *


urlpatterns = [
    url(r'^add_list/(?P<pk>\d+)/$', UserDocListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', UserDocListEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', UserDocListDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', UserDocListRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddDocListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemoveDocListFromUserCollections.as_view()),

    url(r'^create_doc/(?P<pk>\d+)/$', UserDocCreate.as_view()),
    url(r'^edit_doc/(?P<doc_pk>\d+)/$', UserDocEdit.as_view()),
    url(r'^delete_doc/(?P<doc_pk>\d+)/$', UserDocRemove.as_view()),
    url(r'^restore_doc/(?P<doc_pk>\d+)/$', UserDocAbortRemove.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', UserChangeDocPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangeDocListPosition.as_view()),
]
