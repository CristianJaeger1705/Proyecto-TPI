from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import random

from perfiles.models import PerfilCandidato, PerfilEmpresa, ExperienciaLaboral, MUNICIPIOS_POR_DEPARTAMENTO
from ofertas.models import OfertaLaboral
from mensajeria.models import Conversacion
from .forms import FormularioPerfilCandidato, FormularioPerfilEmpresa, FormularioExperienciaLaboral

Usuario = get_user_model()

# -----------------------------
# LOGIN PERSONALIZADO
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirigir según rol y completitud del perfil
            return redirect('usuarios:redirigir_segun_rol')

        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "registration/login.html")


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

        # Procesar nombres
        if rol == "candidato":
            first_name = nombre
            last_name = apellidos
        else:
            first_name = nombre_empresa
            last_name = ""

        # Generar código de verificación
        codigo = str(random.randint(100000, 999999))

        # Guardar datos en sesión
        request.session["registro_data"] = {
            "rol": rol,
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

        return redirect("usuarios:verificar_codigo")

    return render(request, "registration/register.html")


# -----------------------------
# VERIFICAR CÓDIGO DE REGISTRO
# -----------------------------
def verificar_codigo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_verificacion")

        if codigo_ingresado == codigo_correcto:
            data = request.session.get("registro_data")

            # Crear usuario
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
        return redirect("usuarios:verificar_codigo_recuperacion")

    return render(request, "registration/recuperar_contrasena.html")


def verificar_codigo_recuperacion(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_recuperacion")

        if codigo_ingresado == codigo_correcto:
            return redirect("usuarios:nueva_contrasena_recuperacion")

        messages.error(request, "Código incorrecto")

    return render(request, "registration/verificar_codigo_recuperacion.html")


def nueva_contrasena_recuperacion(request):
    if not request.session.get("usuario_recuperacion_id"):
        messages.error(request, "No hay usuario autorizado para cambiar la contraseña.")
        return redirect("usuarios:recuperar_contrasena")

    usuario_id = request.session.get("usuario_recuperacion_id")
    try:
        user = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect("usuarios:recuperar_contrasena")

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
        return redirect("usuarios:login")

    return render(request, "registration/nueva_contrasena_recuperacion.html")


# -----------------------------
# REDIRIGIR SEGÚN ROL
# -----------------------------
@login_required
def redirigir_segun_rol(request):
    user = request.user

    if user.rol == "empresa":
        perfil = PerfilEmpresa.objects.filter(usuario=user).first()
        if perfil and perfil.completado:
            return redirect("perfiles:dashboard_empresa")
        return redirect("perfiles:perfil_empresa")

    if user.rol == "candidato":
        perfil = PerfilCandidato.objects.filter(usuario=user).first()
        if perfil and perfil.completado:
            return redirect("perfiles:dashboard_candidato")
        return redirect("perfiles:perfil_candidato")

    if user.rol == "admin":
        return redirect("/admin/")

    return redirect("/")


# -----------------------------
# PERFILES
# -----------------------------
@login_required
def mi_perfil_candidato(request):
    perfil = getattr(request.user, 'perfil_candidato', None)
    return render(request, 'usuarios/mi_perfil_candidato.html', {'perfil': perfil})


@login_required
def mi_perfil_empresa(request):
    perfil = getattr(request.user, 'perfil_empresa', None)
    return render(request, "usuarios/mi_perfil_empresa.html", {'perfil': perfil})


# -----------------------------
# COMPLETAR / EDITAR PERFILES
# -----------------------------
@login_required
def completar_perfil_candidato(request):
    perfil = getattr(request.user, 'perfil_candidato', None) or PerfilCandidato.objects.create(usuario=request.user)

    if request.method == 'POST':
        form = FormularioPerfilCandidato(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil completado exitosamente! 🎉')
            return redirect('usuarios:mi_perfil_candidato')
    else:
        form = FormularioPerfilCandidato(instance=perfil)

    return render(request, 'usuarios/completar_perfil_candidato.html', {'form': form, 'perfil': perfil})


@login_required
def completar_perfil_empresa(request):
    perfil = getattr(request.user, 'perfil_empresa', None) or PerfilEmpresa.objects.create(usuario=request.user, nombre_empresa=request.user.first_name or 'Mi Empresa')

    if request.method == 'POST':
        form = FormularioPerfilEmpresa(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil de empresa completado exitosamente! 🎉')
            return redirect('usuarios:mi_perfil_empresa')
    else:
        form = FormularioPerfilEmpresa(instance=perfil)

    return render(request, 'usuarios/completar_perfil_empresa.html', {'form': form, 'perfil': perfil})


@login_required
def editar_perfil_candidato(request):
    perfil = getattr(request.user, 'perfil_candidato', None) or PerfilCandidato.objects.create(usuario=request.user)

    if request.method == 'POST':
        form = FormularioPerfilCandidato(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil actualizado exitosamente!')
            return redirect('usuarios:mi_perfil_candidato')
    else:
        form = FormularioPerfilCandidato(instance=perfil)

    return render(request, 'usuarios/editar_perfil_candidato.html', {'form': form, 'perfil': perfil})


@login_required
def editar_perfil_empresa(request):
    perfil = getattr(request.user, 'perfil_empresa', None) or PerfilEmpresa.objects.create(usuario=request.user, nombre_empresa=request.user.first_name or 'Mi Empresa')

    if request.method == 'POST':
        form = FormularioPerfilEmpresa(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil de empresa actualizado exitosamente!')
            return redirect('usuarios:mi_perfil_empresa')
    else:
        form = FormularioPerfilEmpresa(instance=perfil)

    return render(request, 'usuarios/editar_perfil_empresa.html', {'form': form, 'perfil': perfil})


# -----------------------------
# CRUD EXPERIENCIA LABORAL
# -----------------------------
@login_required
def agregar_experiencia(request):
    if request.user.rol != 'candidato':
        messages.error(request, 'Solo los candidatos pueden agregar experiencias laborales.')
        return redirect('pagina_principal')

    perfil = getattr(request.user, 'perfil_candidato', None)
    if not perfil:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('usuarios:completar_perfil_candidato')

    next_url = request.POST.get('next') or request.GET.get('next', 'usuarios:mi_perfil_candidato')

    if request.method == 'POST':
        form = FormularioExperienciaLaboral(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.perfil_candidato = perfil
            experiencia.save()
            messages.success(request, '¡Experiencia laboral agregada exitosamente!')
            return redirect(next_url)
    else:
        form = FormularioExperienciaLaboral()

    return render(request, 'usuarios/form_experiencia.html', {'form': form, 'titulo': 'Agregar Experiencia Laboral', 'accion': 'Agregar', 'next_url': next_url})


@login_required
def editar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id)

    if experiencia.perfil_candidato.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar esta experiencia.')
        return redirect('usuarios:mi_perfil_candidato')

    next_url = request.POST.get('next') or request.GET.get('next', 'usuarios:mi_perfil_candidato')

    if request.method == 'POST':
        form = FormularioExperienciaLaboral(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Experiencia laboral actualizada exitosamente!')
            return redirect(next_url)
    else:
        form = FormularioExperienciaLaboral(instance=experiencia)

    return render(request, 'usuarios/form_experiencia.html', {'form': form, 'experiencia': experiencia, 'titulo': 'Editar Experiencia Laboral', 'accion': 'Actualizar', 'next_url': next_url})


@login_required
def eliminar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id)

    if experiencia.perfil_candidato.usuario != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta experiencia.')
        return redirect('usuarios:mi_perfil_candidato')

    next_url = request.POST.get('next') or request.GET.get('next', 'usuarios:mi_perfil_candidato')

    if request.method == 'POST':
        titulo = experiencia.titulo_cargo
        experiencia.delete()
        messages.success(request, f'Experiencia "{titulo}" eliminada exitosamente.')
        return redirect(next_url)

    return render(request, 'usuarios/confirmar_eliminar_experiencia.html', {'experiencia': experiencia, 'next_url': next_url})


# -----------------------------
# OBTENER MUNICIPIOS POR DEPARTAMENTO (API)
# -----------------------------
def obtener_municipios(request, departamento):
    municipios = MUNICIPIOS_POR_DEPARTAMENTO.get(departamento, [])
    return JsonResponse({'municipios': municipios})


# -----------------------------
# CHAT / MENSAJERÍA
# -----------------------------
def navbar_context(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    chats_privados = Conversacion.objects.filter(participantes=user, grupo=None).distinct()
    return {'chats_privados': chats_privados}


# -----------------------------
# CERRAR SESIÓN
# -----------------------------
def cerrar_sesion(request):
    logout(request)
    return redirect('hola_mundo')


# -----------------------------
# VISTA HOLA MUNDO / INICIO
# -----------------------------
def hola_mundo(request):
    ofertas_recientes = OfertaLaboral.objects.filter(activada=True).order_by('-fecha_publicacion')[:6]
    return render(request, 'hola_mundo.html', {'ofertas_recientes': ofertas_recientes})
