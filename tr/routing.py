from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifications.consumers import NoseyConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("about/", NoseyConsumer),
    ])
})
