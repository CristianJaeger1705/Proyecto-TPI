from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from .models import SolicitudEmpresa
from django.contrib.auth import get_user_model,logout
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth.hashers import make_password


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/nueva_contrasena.html"
    success_url = "/login/"
# Create your views here.

class CustomLoginView(LoginView):
    # 1. Este método se ejecuta cuando el login es EXITOSO
    def form_valid(self, form):
        # Mensaje de éxito
        messages.success(self.request, f"Bienvenido, {form.get_user().first_name} 😄")
        return super().form_valid(form)
    
    # 2. AÑADE ESTE MÉTODO: Se ejecuta cuando el login FALLA (credenciales incorrectas)
    def form_invalid(self, form):
        # Mensaje de error (usará el tag 'error' para el Toast de Bootstrap)
        messages.error(self.request, "Usuario o contraseña inválidos. Inténtalo de nuevo.")
        
        # Llama al método original de la clase padre para re-renderizar la plantilla
        # (Esto pasa el formulario con los errores si los hay, y ahora incluye el mensaje de Toast)
        return super().form_invalid(form)
    
def mi_perfil_candidato(request):
    return render(request, 'usuarios/mi_perfil_candidato.html' )

def mi_perfil_empresa(request):
    return render(request, "usuarios/mi_perfil_empresa.html")

def exit(request):
    logout(request)
    return redirect("login")

Usuario = get_user_model()

def registro(request):
    if request.method == "POST":
        # Obtener datos
        username = request.POST.get("usuario")
        email = request.POST.get("email")
        password = request.POST.get("contrasena")
        confirmar_password = request.POST.get("confirmar_contrasena")
        nombre = request.POST.get("nombre")
        apellidos = request.POST.get("apellidos")
        nombre_empresa = request.POST.get("nombre_empresa")

        # Preparar context para rellenar campos en caso de error
        context = {
            "username": username,
            "email": email,
            "nombre": nombre,
            "apellidos": apellidos,
        }

        # Validaciones
        if password != confirmar_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registration/register.html", context)

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, "registration/register.html", context)

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Ya existe una cuenta con este correo.")
            return render(request, "registration/register.html", context)

        first_name = nombre
        last_name = apellidos

        # Generar código
        codigo = str(random.randint(100000, 999999))

        # Guardar datos en session
        request.session["registro_data"] = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }

        request.session["codigo_verificacion"] = codigo

        # Enviar correo
        send_mail(
            subject="Código de verificación",
            message=f"Tu código es: {codigo}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        messages.success(request, "Se ha enviado un código al correo registrado.")

        return redirect("verificar_codigo")

    return render(request, "registration/register.html")

def crear_cuenta_empresa(request, token):
    solicitud = SolicitudEmpresa.objects.filter(token=token, estado="aprobada").first()

    if not solicitud:
        return render(request, "registration/token_invalido.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["contrasena"]

        user = Usuario.objects.create_user(
                username=username,
                email=solicitud.correo,
                password=password,
                rol="empresa",
                first_name=solicitud.nombre_empresa,
                verificado=False
            )

        return redirect("login")

    return render(request, "registration/registrar_empresa.html", {
        "nombre_empresa": solicitud.nombre_empresa,
        "correo": solicitud.correo,
    })


def redirigir_según_rol(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    if user.rol == "candidato":
        return redirect("mi_perfil_candidato")

    elif user.rol == "empresa":
        return redirect("mi_perfil_empresa")  # la crearás más adelante

    elif user.rol == "admin":
        return redirect("/admin/")

    return redirect("/")  # fallback

def verificar_codigo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_verificacion")

        if codigo_ingresado == codigo_correcto:
            data = request.session.get("registro_data")

            # Crear usuario aquí
            user = Usuario.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                rol=data["rol"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                verificado=False
            )

            # Limpiar session
            request.session.pop("registro_data")
            request.session.pop("codigo_verificacion")

            messages.success(request, "¡Correo verificado exitosamente! 🎉")
            return redirect("login")
        messages.error(request, "Código incorrecto")
        return render(request, "registration/verificar_codigo.html")

    return render(request, "registration/verificar_codigo.html")

def recuperar_contrasena(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return render(request, "registration/recuperar_contrasena.html")

        # Generar código de verificación
        codigo = str(random.randint(100000, 999999))
        request.session['codigo_recuperacion'] = codigo
        request.session['usuario_recuperacion_id'] = user.id

        # Enviar correo
        send_mail(
            subject="Código de recuperación de contraseña",
            message=f"Hola {user.first_name}, tu código es: {codigo}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        messages.success(request, f"Se ha enviado un código al correo registrado.")
        return redirect("verificar_codigo_recuperacion")

    return render(request, "registration/recuperar_contrasena.html")

def verificar_codigo_recuperacion(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_recuperacion")

        if codigo_ingresado == codigo_correcto:
            return redirect("nueva_contrasena_recuperacion")
        else:
            messages.error(request, "Código incorrecto")
            return render(request, "registration/verificar_codigo_recuperacion.html")

    return render(request, "registration/verificar_codigo_recuperacion.html")



Usuario = get_user_model()

def nueva_contrasena_recuperacion(request):
    # Verificamos que exista la sesión con el código validado
    if not request.session.get("usuario_recuperacion_id"):
        messages.error(request, "No hay usuario autorizado para cambiar la contraseña.")
        return redirect("recuperar_contrasena")

    usuario_id = request.session.get("usuario_recuperacion_id")
    try:
        user = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect("recuperar_contrasena")

    if request.method == "POST":
        contrasena = request.POST.get("contrasena")
        confirmar_contrasena = request.POST.get("confirmar_contrasena")

        # Validar que las contraseñas coincidan
        if contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registration/nueva_contrasena_recuperacion.html")

        # Cambiar contraseña
        user.password = make_password(contrasena)
        user.save()

        # Limpiar sesión
        request.session.pop("usuario_recuperacion_id", None)
        request.session.pop("codigo_recuperacion", None)

        messages.success(request, "¡Contraseña cambiada exitosamente! Ahora puedes iniciar sesión.")
        return redirect("login")

    return render(request, "registration/nueva_contrasena_recuperacion.html")

def solicitar_empresa(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre_empresa")
        sitio = request.POST.get("sitio_web")
        correo = request.POST.get("correo_corporativo")
        descripcion = request.POST.get("descripcion")
        telefono = request.POST.get("telefono")

        SolicitudEmpresa.objects.create(
            nombre_empresa=nombre,
            telefono=telefono,
            sitio_web=sitio,
            correo=correo,
            descripcion=descripcion,
            solicitante=request.user if request.user.is_authenticated else None
        )

        messages.success(request, "Solicitud enviada. Será revisada por un administrador.")
        return redirect("login")

    return render(request, "registration/solicitar_empresa.html")

