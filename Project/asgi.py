"""
ASGI config for Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter ,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

django_asgi_app = get_asgi_application()

from chat import routing as chat_routing
from videochat import routing as videochat_routing

application = ProtocolTypeRouter({
    "http" : django_asgi_app,
    "websocket" : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(chat_routing.websocket_urlpatterns + videochat_routing.websocket_urlpatterns)
            )
    )
})

