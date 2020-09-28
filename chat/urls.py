from django.conf.urls import url, include
from chat.views import *


urlpatterns = [
    url(r'^$', MessagesListView.as_view(), name='messages_list'),
    url(r'^(?P<pk>\d+)/$', ChatDetailView.as_view(), name='chat_detali'),

    url(r'^message_progs/', include('posts.url.message_progs')),
	#url(r'^chat_progs/', include('posts.url.chat_progs')),
    #url(r'^member_progs/', include('posts.url.member_progs')),
]
