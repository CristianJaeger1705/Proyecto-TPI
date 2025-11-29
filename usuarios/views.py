from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from ofertas.models import OfertaLaboral

Usuario = get_user_model()

# -----------------------------
# LOGIN PERSONALIZADO
# -----------------------------
from perfiles.models import PerfilCandidato, PerfilEmpresa

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from perfiles.models import PerfilCandidato, PerfilEmpresa

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # --- PERFIL CANDIDATO ---
            if user.rol == "candidato":
                perfil, created = PerfilCandidato.objects.get_or_create(usuario=user)
                print("Perfil Candidato:", perfil, perfil.completado)
                if perfil.completado:
                    return redirect("perfiles:dashboard_candidato")
                return redirect("perfiles:perfil_candidato")

            # --- PERFIL EMPRESA ---
            elif user.rol == "empresa":
                perfil, created = PerfilEmpresa.objects.get_or_create(
                    usuario=user,
                    defaults={"nombre_empresa": user.first_name or user.username}
                )
                print("Perfil Empresa:", perfil, perfil.completado)
                if perfil.completado:
                    return redirect("perfiles:dashboard_empresa")
                return redirect("perfiles:perfil_empresa")

            # --- ADMIN ---
            elif user.rol == "admin":
                return redirect("/admin/")

            return redirect("/")

        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "registration/login.html")




class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/nueva_contrasena.html"
    success_url = "/login/"


# -----------------------------
# PERFILES
# -----------------------------
def mi_perfil_candidato(request):
    return render(request, 'usuarios/mi_perfil_candidato.html')

def mi_perfil_empresa(request):
    return render(request, "usuarios/mi_perfil_empresa.html")



def cerrar_sesion(request):
    logout(request)
    return redirect('hola_mundo')


# -----------------------------
# REGISTRO
# -----------------------------
def registro(request):
    if request.method == "POST":

        rol = request.POST.get("rol")
        username = request.POST.get("usuario")
        email = request.POST.get("email")
        password = request.POST.get("contrasena")
        confirmar_password = request.POST.get("confirmar_contrasena")
        nombre = request.POST.get("nombre")
        apellidos = request.POST.get("apellidos")
        nombre_empresa = request.POST.get("nombre_empresa")

        context = {
            "rol": rol,
            "username": username,
            "email": email,
            "nombre": nombre,
            "apellidos": apellidos,
            "nombre_empresa": nombre_empresa
        }

        if password != confirmar_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registration/register.html", context)

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, "registration/register.html", context)

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Ya existe una cuenta con este correo.")
            return render(request, "registration/register.html", context)

        if rol == "candidato":
            first_name = nombre
            last_name = apellidos
        else:
            first_name = nombre_empresa
            last_name = ""

        codigo = str(random.randint(100000, 999999))

        request.session["registro_data"] = {
            "rol": rol,
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }

        request.session["codigo_verificacion"] = codigo

        send_mail(
            subject="Código de verificación",
            message=f"Tu código es: {codigo}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        messages.success(request, "Se ha enviado un código al correo registrado.")

        return redirect("usuarios:verificar_codigo")  # ← FIX NAMESPACE

    return render(request, "registration/register.html")


# -----------------------------
# REDIRIGIR POR ROL
# -----------------------------

@login_required
def redirigir_segun_rol(request):
    user = request.user

    # Empresa
    if user.rol == "empresa":
        perfil = PerfilEmpresa.objects.filter(usuario=user).first()

        if perfil and perfil.completado:
            return redirect("perfiles:dashboard_empresa")
        return redirect("perfiles:perfil_empresa")

    # Candidato
    if user.rol == "candidato":
        perfil = PerfilCandidato.objects.filter(usuario=user).first()

        if perfil and perfil.completado:
            return redirect("perfiles:dashboard_candidato")
        return redirect("perfiles:perfil_candidato")

    # Admin
    if user.rol == "admin":
        return redirect("/admin/")

    return redirect("/")




# -----------------------------
# VERIFICAR CÓDIGO DE REGISTRO
# -----------------------------

def verificar_codigo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_verificacion")

        if codigo_ingresado == codigo_correcto:
            data = request.session.get("registro_data")

            user = Usuario.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                rol=data["rol"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                verificado=True
            )

            # Crear perfil inicial según rol
            if user.rol == "candidato":
                PerfilCandidato.objects.create(usuario=user)
                redirect_url = "perfiles:completar_perfil_candidato"
            elif user.rol == "empresa":
                PerfilEmpresa.objects.create(usuario=user, nombre_empresa=data["first_name"])
                redirect_url = "perfiles:completar_perfil_empresa"
            else:
                redirect_url = "usuarios:login"

            # Limpiar sesión
            request.session.pop("registro_data")
            request.session.pop("codigo_verificacion")

            messages.success(request, "¡Correo verificado exitosamente! 🎉")

            # Redirigir a completar perfil inmediatamente
            return redirect(redirect_url)

        messages.error(request, "Código incorrecto")

    return render(request, "registration/verificar_codigo.html")

# -----------------------------
# RECUPERAR CONTRASEÑA
# -----------------------------
def recuperar_contrasena(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return render(request, "registration/recuperar_contrasena.html")

        codigo = str(random.randint(100000, 999999))
        request.session['codigo_recuperacion'] = codigo
        request.session['usuario_recuperacion_id'] = user.id

        send_mail(
            subject="Código de recuperación de contraseña",
            message=f"Hola {user.first_name}, tu código es: {codigo}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        messages.success(request, "Se ha enviado un código al correo registrado.")
        return redirect("usuarios:verificar_codigo_recuperacion")  # ← FIX

    return render(request, "registration/recuperar_contrasena.html")


def verificar_codigo_recuperacion(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_recuperacion")

        if codigo_ingresado == codigo_correcto:
            return redirect("usuarios:nueva_contrasena_recuperacion")  # ← FIX
        else:
            messages.error(request, "Código incorrecto")

    return render(request, "registration/verificar_codigo_recuperacion.html")


def nueva_contrasena_recuperacion(request):

    if not request.session.get("usuario_recuperacion_id"):
        messages.error(request, "No hay usuario autorizado para cambiar la contraseña.")
        return redirect("usuarios:recuperar_contrasena")  # ← FIX

    usuario_id = request.session.get("usuario_recuperacion_id")
    try:
        user = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect("usuarios:recuperar_contrasena")  # ← FIX

    if request.method == "POST":
        contrasena = request.POST.get("contrasena")
        confirmar_contrasena = request.POST.get("confirmar_contrasena")

        if contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registration/nueva_contrasena_recuperacion.html")

        user.password = make_password(contrasena)
        user.save()

        request.session.pop("usuario_recuperacion_id", None)
        request.session.pop("codigo_recuperacion", None)

        messages.success(request, "¡Contraseña cambiada exitosamente! Ahora puedes iniciar sesión.")
        return redirect("usuarios:login")  # ← FIX

    return render(request, "registration/nueva_contrasena_recuperacion.html")


def hola_mundo(request):
    # Tomar solo las 6 últimas ofertas activas
    ofertas_recientes = OfertaLaboral.objects.filter(activada=True).order_by('-fecha_publicacion')[:6]
    return render(request, 'hola_mundo.html', {'ofertas_recientes': ofertas_recientes})


from mensajeria.models import Conversacion

def navbar_context(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    # Chats privados donde participa
    chats_privados = Conversacion.objects.filter(
        participantes=user,
        grupo=None  # importante: solo privados
    ).distinct()

    return {
        'chats_privados': chats_privados,
    }
