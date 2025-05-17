from django.urls import re_path, include
from chat.views import *


urlpatterns = [
    re_path(r'^$', ChatsListView.as_view(), name='chats_list'),
    re_path(r'^closed_support_chats/$', ClosedSupportChats.as_view()),
    re_path(r'^(?P<pk>\d+)/$', ChatDetailView.as_view(), name='chat_detail'),
    re_path(r'^(?P<pk>\d+)/fixed_messages/$', ChatFixedMessagesView.as_view()),
    re_path(r'^(?P<pk>\d+)/info/$', ChatInfo.as_view()),
    re_path(r'^(?P<pk>\d+)/collections/$', ChatCollections.as_view()),
    re_path(r'^favourites_messages/$', ChatFavouritesMessagesView.as_view()),
    re_path(r'^(?P<pk>\d+)/search/$', ChatSearchView.as_view()),

    re_path(r'^user_progs/', include('chat.url.user_progs')),
]
