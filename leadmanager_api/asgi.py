# leadmanager_api/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import leads.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leadmanager_api.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            leads.routing.websocket_urlpatterns
        )
    ),
})
