"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""


import os
from chatrooms import  routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatrooms.middleware import TokenAuthMiddleware
# from chatrooms.middleware import JWTAuthMiddleware
from channels.security.websocket import AllowedHostsOriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': application,
    'websocket':
        AuthMiddlewareStack(
            TokenAuthMiddleware(
                URLRouter(
                    routing.websocket_urlpatterns
                )
            )
        )
    ,

})