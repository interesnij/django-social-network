from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from notify.consumers import NotificationsConsumer
from chat.consumers import MessagerConsumer


application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url("ws://xn--80aa0cf.xn--p1acf:8002/notify/", NotificationsConsumer),
                #url('ws://раса.рус/(?P<username>[^/]+)/$', MessagerConsumer),
            ])
        ),
    ),
})
