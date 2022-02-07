from django.conf.urls import url
from docs.views import *


urlpatterns = [
    url(r'^$', DocsView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadDocList.as_view(), name="load_doc_list"),

    url(r'^add_docs_in_list/(?P<pk>\d+)/$', AddDocInList.as_view()),
    url(r'^edit_doc/(?P<pk>\d+)/$', DocEdit.as_view()),
    url(r'^delete_doc/(?P<pk>\d+)/$', DocRemove.as_view()),
    url(r'^restore_doc/(?P<pk>\d+)/$', DocRestore.as_view()),
]
