from django.conf.urls import url
from chat import *


urlpatterns = [
    url(r'^$', MessagesListView.as_view(), name='messages_list'),
    url(r'^(?P<uuid>[0-9a-f-]+)/$', ChatDetailView.as_view(), name='chat_detali'),
]
