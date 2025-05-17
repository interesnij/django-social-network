from django.urls import re_path
from docs.views import *


urlpatterns = [
    re_path(r'^$', DocsView.as_view()),
    re_path(r'^load_list/(?P<pk>\d+)/$', LoadDocList.as_view(), name="load_doc_list"),

    re_path(r'^add_docs_in_list/(?P<pk>\d+)/$', AddDocInList.as_view()),
    re_path(r'^edit_doc/(?P<pk>\d+)/$', DocEdit.as_view()),
    re_path(r'^delete_doc/(?P<pk>\d+)/$', DocRemove.as_view()),
    re_path(r'^restore_doc/(?P<pk>\d+)/$', DocRestore.as_view()),
]
