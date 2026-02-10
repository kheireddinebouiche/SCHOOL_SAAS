
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .asgi_middleware import TenantAuthMiddleware
import institut_app.routing
# from django_tenants.middleware.asgi import TenantMainMiddleware # Only if using tenant schemas in websockets, which is tricky. 
# For now, let's assume we might need to handle tenancy manually or via a custom middleware if django-tenants has no direct ASGI support out of the box that is stable.
# However, standard practice with django-tenants is that the domain identifies the tenant.
# We will use a basic setup first.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TenantAuthMiddleware(
        URLRouter(
            institut_app.routing.websocket_urlpatterns
        )
    ),
})
