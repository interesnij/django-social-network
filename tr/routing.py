from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat.consumers import MessagerConsumer
from notifications.consumers import NotificationsConsumer


application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url(r'^ws/notifications/$', NotificationsConsumer),
                url(r'^ws/(?P<username>[^/]+)/$', MessagerConsumer),
            ])
        ),
    ),
})
