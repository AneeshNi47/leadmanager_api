from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from leads import consumers  # Replace with your actual import

websocket_urlpatterns = [
    path("ws/leads/", consumers.LeadsConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
