from django.conf.urls import url
from docs.view.user_progs import *


urlpatterns = [
    url(r'^create_doc/(?P<pk>\d+)/$', UserDocCreate.as_view()),
    url(r'^edit_doc/(?P<doc_pk>\d+)/$', UserDocEdit.as_view()),
    url(r'^delete_doc/(?P<doc_pk>\d+)/$', UserDocRemove.as_view()),
    url(r'^restore_doc/(?P<doc_pk>\d+)/$', UserDocAbortRemove.as_view()),
]
