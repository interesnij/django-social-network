from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifiocation.consumers import NoseyConsumer, ws_connect

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/", NoseyConsumer),
        "websocket.connect": consumers.ws_connect,
    ])
})
