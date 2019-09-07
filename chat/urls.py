from django.conf.urls import url

from chat.views import *

app_name = 'chat'

urlpatterns = [
    url(r'^$', MessagesListView.as_view(), name='messages_list'),
    url(r'^send-message/$', send_message, name='send_message'),
    url(r'^receive-message/$', receive_message, name='receive_message'),
    url(r'^(?P<id>[\w.@+-]+)/$', ConversationListView.as_view(), name='conversation_detail'),
]
