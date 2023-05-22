import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revista.settings')

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(notifications.routing.websocket_urlpatterns))
        ),
    }
)
