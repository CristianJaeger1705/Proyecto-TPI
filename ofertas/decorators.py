from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def empresa_o_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, "Debe iniciar sesión para acceder.")
            return redirect('login')

        if request.user.rol not in ['admin', 'empresa']:
            messages.error(request, "No tiene permisos para acceder a esta sección.")
            return redirect('lista_ofertas_publicas')

        return view_func(request, *args, **kwargs)
    return wrapper
