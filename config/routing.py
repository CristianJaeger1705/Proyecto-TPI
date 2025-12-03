from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mensajeria.routing  # importa tu routing de la app mensajeria

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mensajeria.routing.websocket_urlpatterns
        )
    ),
})
