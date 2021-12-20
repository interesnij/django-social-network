from django.conf.urls import url, include
from chat.views import *


urlpatterns = [
    url(r'^$', ChatsListView.as_view(), name='chats_list'),
    url(r'^(?P<pk>\d+)/$', ChatDetailView.as_view(), name='chat_detail'),
    url(r'^(?P<pk>\d+)/fixed_messages/$', ChatFixedMessagesView.as_view()),
    url(r'^(?P<pk>\d+)/info/$', ChatInfo.as_view()),
    url(r'^(?P<pk>\d+)/collections/$', ChatCollections.as_view()),
    url(r'^favourites_messages/$', ChatFavouritesMessagesView.as_view()),
    url(r'^(?P<pk>\d+)/search/$', ChatSearchView.as_view()),

    url(r'^user_progs/', include('chat.url.user_progs')),
]
