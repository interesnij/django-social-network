from django.conf.urls import url, include
from chat.view.chat_progs import *


urlpatterns = [
    url(r'^create_chat/(?P<pk>\d+)/$', CreateChat.as_view()),
    #url(r'^edit/(?P<pk>\d+)/$', ChatEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', ChatDelete.as_view()),
	url(r'^restore/(?P<pk>\d+)/$', ChatRecover.as_view()),
    url(r'^exit/(?P<pk>\d+)/$', ChatExit.as_view()),
]
