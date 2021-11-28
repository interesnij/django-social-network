from django.conf.urls import url, include
from chat.views import *


urlpatterns = [
    url(r'^$', MessagesListView.as_view(), name='messages_list'),
    url(r'^(?P<pk>\d+)/$', ChatDetailView.as_view(), name='chat_detail'),
    url(r'^(?P<pk>\d+)/fixed_messages/$', ChatFixedMessagesView.as_view()),
    url(r'^(?P<pk>\d+)/info/$', ChatInfo.as_view()),

    url(r'^user_progs/', include('chat.url.user_progs')),
]
