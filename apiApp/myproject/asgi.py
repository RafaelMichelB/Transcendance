import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # Import manquant pour AuthMiddlewareStack
from api.routing import websocket_urlpatterns  # Import du fichier de routing WebSocket


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # WebSockets avec authentification Django
        URLRouter(websocket_urlpatterns)
    ),
})

