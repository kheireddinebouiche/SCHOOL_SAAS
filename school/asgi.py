import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from .asgi_middleware import TenantAuthMiddleware
import institut_app.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TenantAuthMiddleware(
        URLRouter(
            institut_app.routing.websocket_urlpatterns
        )
    ),
})
