from django.conf.urls import url
from docs.view.community_progs import *


urlpatterns = [
    url(r'^create_doc/(?P<pk>\d+)/$', CommunityDocCreate.as_view()),
    url(r'^edit_doc/(?P<doc_pk>\d+)/$', CommunityDocEdit.as_view()),
    url(r'^delete_doc/(?P<doc_pk>\d+)/$', CommunityDocRemove.as_view()),
    url(r'^restore_doc/(?P<doc_pk>\d+)/$', CommunityDocAbortRemove.as_view()),
]
