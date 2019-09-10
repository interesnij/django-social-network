from django.conf.urls import url
from django.urls import path
from chat.views import *



urlpatterns = [
    path(r'', MessagesListView.as_view(), name='messages_list'),
    path('<str:room_name>/', room, name='room'),
]
