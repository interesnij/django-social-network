from django.conf.urls import url
from docs.view.user_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^create_list_window/(?P<pk>\d+)/$', UserCreateDoclistWindow.as_view()),

    url(r'^create_list/(?P<pk>\d+)/$', UserDoclistCreate.as_view()),

    url(r'^u_add_doc/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocAdd.as_view())),
    url(r'^u_remove_doc/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocRemove.as_view())),
    url(r'^u_add_doc_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocListAdd.as_view())),
    url(r'^u_remove_doc_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocListRemove.as_view())),
]
