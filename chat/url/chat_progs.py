from django.conf.urls import url, include
from chat.view.chat_progs import *


urlpatterns = [
    url(r'^create_chat/$', login_required(CreateChat.as_view())),
    url(r'^edit/(?P<pk>\d+)/$', login_required(ChatEdit.as_view())),
    url(r'^delete/(?P<pk>\d+)/$', login_required(ChatDelete.as_view())),
	url(r'^abort_delete/(?P<pk>\d+)/$', login_required(ChatAbortDelete.as_view())),
    url(r'^exit/(?P<pk>\d+)/$', login_required(ChatExit.as_view())),
]
