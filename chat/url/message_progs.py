from django.conf.urls import url, include
from chat.view.message_progs import *


urlpatterns = [
    url(r'^send_page_message/(?P<pk>\d+)/$', SendPageMessage.as_view()),
    #url(r'^send_page_manager_message/$', SendPageManagerMessage.as_view()),
    url(r'^send_message/(?P<pk>\d+)/$', SendMessage.as_view()),
    url(r'^forvard_message/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageForvard.as_view())),
    #url(r'^edit/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageEdit.as_view())),

    url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageFixed.as_view())),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageUnFixed.as_view())),
    url(r'^favorite/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageFavorite.as_view())),
    url(r'^unfavorite/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageUnFavorite.as_view())),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageDelete.as_view())),
	url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(MessageAbortDelete.as_view())),
]
