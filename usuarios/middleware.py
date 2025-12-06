from django.shortcuts import redirect
from django.urls import reverse

class RedirectDjangoLoginMiddleware:
    """
    Redirige cualquier acceso a /accounts/login/ al login personalizado.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si alguien va al login por defecto de Django, redirige
        if request.path == '/accounts/login/':
            return redirect(reverse('usuarios:login'))
        
        response = self.get_response(request)
        return response
