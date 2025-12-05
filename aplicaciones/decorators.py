from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def solo_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 1️⃣ Si no está logueado → al login
        if not request.user.is_authenticated:
            return redirect("usuarios:login")

        # 2️⃣ Si está logueado pero NO es admin → página principal
        if request.user.rol != "admin":
            return redirect("pagina_principal")  # O donde quieras enviarlo

        # 3️⃣ Si es admin → permitir acceso
        return view_func(request, *args, **kwargs)
    return wrapper
