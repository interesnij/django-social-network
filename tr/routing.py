from django.urls import re_path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from notify.consumers import NotificationsConsumer
from chat.consumers import MessagerConsumer


application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r"^notify/$", NotificationsConsumer.as_asgi()),
                #url('ws://раса.рус/(?P<username>[^/]+)/$', MessagerConsumer),
            ])
        ),
    ),
})
