"""
ASGI config for sudoku project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import sudokubattle.routing 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sudoku.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
  AuthMiddlewareStack(
        URLRouter(
            sudokubattle.routing.websocket_urlpatterns
        )
  )
  ),
})