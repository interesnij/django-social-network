from django.conf.urls import url, include
from chat.view.user_progs import *


urlpatterns = [
    url(r'^send_page_message/(?P<pk>\d+)/$', SendPageMessage.as_view()),
    #url(r'^send_page_manager_message/$', SendPageManagerMessage.as_view()),
    url(r'^send_message/(?P<pk>\d+)/$', SendMessage.as_view()),
    url(r'^parent_message/(?P<uuid>[0-9a-f-]+)/$', MessageParent.as_view()),
    #url(r'^edit/(?P<uuid>[0-9a-f-]+)/$', MessageEdit.as_view()),
    url(r'^load_chat_message/(?P<uuid>[0-9a-f-]+)/$', LoadUserChatMessage.as_view()),
    url(r'^load_message/(?P<uuid>[0-9a-f-]+)/$', LoadUserMessage.as_view()),

    url(r'^create_chat/(?P<pk>\d+)/$', CreateUserChat.as_view()),

    url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', MessageFixed.as_view()),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', MessageUnFixed.as_view()),
    url(r'^favorite/(?P<uuid>[0-9a-f-]+)/$', MessageFavorite.as_view()),
    url(r'^unfavorite/(?P<uuid>[0-9a-f-]+)/$', MessageUnFavorite.as_view()),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', MessageDelete.as_view()),
	url(r'^restore/(?P<uuid>[0-9a-f-]+)/$', MessageRecover.as_view()),
]
