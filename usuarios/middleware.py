from django.utils import timezone

class UltimaConexionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Solo actualizar si:
        # - El usuario está autenticado
        # - La request NO es logout
        if request.user.is_authenticated and request.path != '/usuarios/logout/':
            request.user.last_seen = timezone.now()
            request.user.save(update_fields=["last_seen"])

        return response
