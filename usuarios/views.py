from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,logout
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import SolicitudEmpresa
from .forms import ReviewForm
from .models import Review
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Review, Candidato

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/nueva_contrasena.html"
    success_url = "/login/"
# Create your views here.

def es_admin(user):
    return user.is_authenticated and user.rol == "admin"

@user_passes_test(es_admin)
def listar_reseñas(request):
    reseñas = Review.objects.select_related("candidato").order_by("-fecha")
    return render(request, "listar_reseñas.html", {
        "reseñas": reseñas
    })



#formulario para dejar review
@login_required
def crear_reseña(request):
    if request.user.rol != "candidato":
        return redirect("pagina_principal")

    candidato = Candidato.objects.get(usuario=request.user)

    if request.method == "POST":
        Review.objects.create(
            candidato=candidato,
            calificacion=request.POST["calificacion"],
            comentario=request.POST["comentario"]
        )
        return redirect("pagina_principal")

    return render(request, "dejar_reseñas.html")





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
    
@login_required
def mi_perfil_candidato(request):
    """Vista para ver el perfil del candidato actual"""
    try:
        perfil = request.user.perfil_candidato
    except:
        # Si no existe el perfil, crear uno automáticamente
        from perfiles.models import PerfilCandidato
        perfil = PerfilCandidato.objects.create(usuario=request.user)
    
    context = {
        'perfil': perfil,
        'habilidades_lista': perfil.get_habilidades_lista(),
    }
    return render(request, 'usuarios/mi_perfil_candidato.html', context)

@login_required
def mi_perfil_empresa(request):
    """Vista para ver el perfil de la empresa actual"""
    try:
        perfil = request.user.perfil_empresa
    except:
        # Si no existe el perfil, crear uno automáticamente
        from perfiles.models import PerfilEmpresa
        perfil = PerfilEmpresa.objects.create(
            usuario=request.user,
            nombre_empresa=request.user.first_name or 'Mi Empresa'
        )
    
    context = {
        'perfil': perfil,
    }
    return render(request, "usuarios/mi_perfil_empresa.html", context)


# ============================================
# VISTAS PARA COMPLETAR PERFILES
# ============================================

@login_required
def completar_perfil_candidato(request):
    """
    Vista para que el candidato complete su perfil después del registro
    """
    try:
        perfil = request.user.perfil_candidato
    except:
        from perfiles.models import PerfilCandidato
        perfil = PerfilCandidato.objects.create(usuario=request.user)
    
    if request.method == 'POST':
        from .forms import FormularioPerfilCandidato
        form = FormularioPerfilCandidato(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            # Verificar completitud y marcar como completo
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil completado exitosamente! 🎉')
            return redirect('usuarios:mi_perfil_candidato')
    else:
        from .forms import FormularioPerfilCandidato
        form = FormularioPerfilCandidato(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'usuarios/completar_perfil_candidato.html', context)


@login_required
def completar_perfil_empresa(request):
    """
    Vista para que la empresa complete su perfil después del registro
    """
    try:
        perfil = request.user.perfil_empresa
    except:
        from perfiles.models import PerfilEmpresa
        perfil = PerfilEmpresa.objects.create(
            usuario=request.user,
            nombre_empresa=request.user.first_name or 'Mi Empresa'
        )
    
    if request.method == 'POST':
        from .forms import FormularioPerfilEmpresa
        form = FormularioPerfilEmpresa(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            # Verificar completitud
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil de empresa completado exitosamente! 🎉')
            return redirect('usuarios:mi_perfil_empresa')
    else:
        from .forms import FormularioPerfilEmpresa
        form = FormularioPerfilEmpresa(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'usuarios/completar_perfil_empresa.html', context)


# ============================================
# VISTAS PARA EDITAR PERFILES
# ============================================

@login_required
def editar_perfil_candidato(request):
    """
    Vista para editar el perfil del candidato
    """
    try:
        perfil = request.user.perfil_candidato
    except:
        from perfiles.models import PerfilCandidato
        perfil = PerfilCandidato.objects.create(usuario=request.user)
    
    if request.method == 'POST':
        from .forms import FormularioPerfilCandidato
        form = FormularioPerfilCandidato(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil actualizado exitosamente!')
            return redirect('usuarios:mi_perfil_candidato')
    else:
        from .forms import FormularioPerfilCandidato
        form = FormularioPerfilCandidato(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'usuarios/editar_perfil_candidato.html', context)


@login_required
def editar_perfil_empresa(request):
    """
    Vista para editar el perfil de la empresa
    """
    try:
        perfil = request.user.perfil_empresa
    except:
        from perfiles.models import PerfilEmpresa
        perfil = PerfilEmpresa.objects.create(
            usuario=request.user,
            nombre_empresa=request.user.first_name or 'Mi Empresa'
        )
    
    if request.method == 'POST':
        from .forms import FormularioPerfilEmpresa
        form = FormularioPerfilEmpresa(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            perfil.verificar_completitud()
            messages.success(request, '¡Perfil de empresa actualizado exitosamente!')
            return redirect('usuarios:mi_perfil_empresa')
    else:
        from .forms import FormularioPerfilEmpresa
        form = FormularioPerfilEmpresa(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'usuarios/editar_perfil_empresa.html', context)

def exit(request):
    logout(request)
    return redirect('pagina_principal')

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

        # Procesar nombres
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
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        messages.success(request, "Se ha enviado un código al correo registrado.")

        return redirect("usuarios:verificar_codigo")

    return render(request, "registration/register.html")

def crear_cuenta_empresa(request, token):
    solicitud = SolicitudEmpresa.objects.filter(token=token, estado="aprobada").first()

    if not solicitud:
        return render(request, "registration/token_invalido.html")

    if request.method == "POST":
        username = request.POST.get("usuario")
        password = request.POST.get("contrasena")
        confirmar_password = request.POST.get("confirmar_contrasena")

        context = {
            "username": username,
        }

        if password != confirmar_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registration/registrar_empresa.html", {
                "username": username,
                "token": token, 
            })
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, "registration/registrar_empresa.html", {
                "token": token,  
            })

        user = Usuario.objects.create_user(
                username=username,
                email=solicitud.correo,
                password=password,
                rol="empresa",
                first_name=solicitud.nombre_empresa,
                verificado=False
            )

        return redirect("usuarios:login")

    return render(request, "registration/registrar_empresa.html", {
        "nombre_empresa": solicitud.nombre_empresa,
        "correo": solicitud.correo,
        "token": solicitud.token,
    })



def solicitar_empresa(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre_empresa")
        sitio = request.POST.get("sitio_web")
        correo = request.POST.get("correo_corporativo")
        descripcion = request.POST.get("descripcion")
        telefono = request.POST.get("telefono")

        context = {
            "nombre_empresa": nombre,
            "telefono": telefono,
            "sitio_web": sitio,
            "correo": correo,
            "descripcion" : descripcion,
        }

        # If unicidad
        if Usuario.objects.filter(email=correo).exists():
            messages.error(request, "Ya existe una empresa con este correo.")
            return render(request, "registration/solicitar_empresa.html", context)

        solicitud_existente = SolicitudEmpresa.objects.filter(correo=correo).first()

        if solicitud_existente and solicitud_existente.estado == "pendiente":
            messages.error(request, "Ya se envio una solicitud con ese correo.")
            return render(request, "registration/solicitar_empresa.html", context)
        
        if solicitud_existente and solicitud_existente.estado == "aprobada":
            messages.success(request, "Se aprobo su solicitud revise su correo para finalizar registro")
            return render(request, "registration/solicitar_empresa.html", context)


        SolicitudEmpresa.objects.create(
            nombre_empresa=nombre,
            telefono=telefono,
            sitio_web=sitio,
            correo=correo,
            descripcion=descripcion,
            solicitante=request.user if request.user.is_authenticated else None
        )

        messages.success(request, "Solicitud enviada. Será revisada por un administrador.")
        return redirect("usuarios:login")

    return render(request, "registration/solicitar_empresa.html")

def redirigir_según_rol(request):
    """
    Redirige al usuario según su rol y si tiene el perfil completo
    """
    user = request.user

    if not user.is_authenticated:
        return redirect("usuarios:login")

    if user.rol == "candidato":
        # Verificar si tiene perfil completo
        try:
            perfil = user.perfil_candidato
            if not perfil.perfil_completo:
                # Si no está completo, redirigir a completar perfil
                return redirect("usuarios:completar_perfil_candidato")
        except:
            # Si no existe perfil (por alguna razón), obtener o crear
            from perfiles.models import PerfilCandidato
            perfil, created = PerfilCandidato.objects.get_or_create(usuario=user)
            return redirect("usuarios:completar_perfil_candidato")
        
        return redirect("usuarios:mi_perfil_candidato")

    elif user.rol == "empresa":
        # Verificar si tiene perfil completo
        try:
            perfil = user.perfil_empresa
            if not perfil.perfil_completo:
                # Si no está completo, redirigir a completar perfil
                return redirect("usuarios:completar_perfil_empresa")
        except:
            # Si no existe perfil (por alguna razón), obtener o crear
            from perfiles.models import PerfilEmpresa
            perfil, created = PerfilEmpresa.objects.get_or_create(
                usuario=user,
                defaults={'nombre_empresa': user.first_name or 'Mi Empresa'}
            )
            return redirect("usuarios:completar_perfil_empresa")
        
        return redirect("usuarios:mi_perfil_empresa")

    elif user.rol == "admin":
        return redirect("/admin/")

    return redirect("pagina_principal")  # fallback

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
                verificado=True
            )

            # Limpiar session
            request.session.pop("registro_data")
            request.session.pop("codigo_verificacion")

            messages.success(request, "¡Correo verificado exitosamente!")
            return redirect("usuarios:login")
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
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        messages.success(request, f"Se ha enviado un código al correo registrado.")
        return redirect("usuarios:verificar_codigo_recuperacion")

    return render(request, "registration/recuperar_contrasena.html")

def verificar_codigo_recuperacion(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_correcto = request.session.get("codigo_recuperacion")

        if codigo_ingresado == codigo_correcto:
            return redirect("usuarios:nueva_contrasena_recuperacion")
        else:
            messages.error(request, "Código incorrecto")
            return render(request, "registration/verificar_codigo_recuperacion.html")

    return render(request, "registration/verificar_codigo_recuperacion.html")



Usuario = get_user_model()

def nueva_contrasena_recuperacion(request):
    # Verificamos que exista la sesión con el código validado
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
        return redirect("usuarios:login")

    return render(request, "registration/nueva_contrasena_recuperacion.html")


# ============================================
# VISTAS CRUD: EXPERIENCIA LABORAL
# ============================================

@login_required
def agregar_experiencia(request):
    """Vista para agregar una nueva experiencia laboral"""
    if request.user.rol != 'candidato':
        messages.error(request, 'Solo los candidatos pueden agregar experiencias laborales.')
        return redirect('pagina_principal')
    
    try:
        perfil = request.user.perfil_candidato
    except:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('usuarios:completar_perfil_candidato')
    
    # Obtener la URL de retorno (de GET o POST)
    next_url = request.POST.get('next') or request.GET.get('next', 'usuarios:mi_perfil_candidato')
    
    if request.method == 'POST':
        from .forms import FormularioExperienciaLaboral
        form = FormularioExperienciaLaboral(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.perfil_candidato = perfil
            experiencia.save()
            messages.success(request, '¡Experiencia laboral agregada exitosamente!')
            return redirect(next_url)
    else:
        from .forms import FormularioExperienciaLaboral
        form = FormularioExperienciaLaboral()
    
    context = {
        'form': form,
        'titulo': 'Agregar Experiencia Laboral',
        'accion': 'Agregar',
        'next_url': next_url,
    }
    return render(request, 'usuarios/form_experiencia.html', context)


@login_required
def editar_experiencia(request, experiencia_id):
    """Vista para editar una experiencia laboral existente"""
    from perfiles.models import ExperienciaLaboral
    from django.shortcuts import get_object_or_404
    
    experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id)
    
    # Verificar que la experiencia pertenece al usuario actual
    if experiencia.perfil_candidato.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar esta experiencia.')
        return redirect('usuarios:mi_perfil_candidato')
    
    # Obtener la URL de retorno (de GET o POST)
    next_url = request.POST.get('next') or request.GET.get('next', 'usuarios:mi_perfil_candidato')
    
    if request.method == 'POST':
        from .forms import FormularioExperienciaLaboral
        form = FormularioExperienciaLaboral(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Experiencia laboral actualizada exitosamente!')
            return redirect(next_url)
    else:
        from .forms import FormularioExperienciaLaboral
        form = FormularioExperienciaLaboral(instance=experiencia)
    
    context = {
        'form': form,
        'experiencia': experiencia,
        'titulo': 'Editar Experiencia Laboral',
        'accion': 'Actualizar',
        'next_url': next_url,
    }
    return render(request, 'usuarios/form_experiencia.html', context)


@login_required
def eliminar_experiencia(request, experiencia_id):
    """Vista para eliminar una experiencia laboral"""
    from perfiles.models import ExperienciaLaboral
    from django.shortcuts import get_object_or_404
    
    experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id)
    
    # Verificar que la experiencia pertenece al usuario actual
    if experiencia.perfil_candidato.usuario != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta experiencia.')
        return redirect('usuarios:mi_perfil_candidato')
    
    # Obtener la URL de retorno (de GET o POST)
    next_url = request.POST.get('next') or request.GET.get('next', 'usuarios:mi_perfil_candidato')
    
    if request.method == 'POST':
        titulo = experiencia.titulo_cargo
        experiencia.delete()
        messages.success(request, f'Experiencia "{titulo}" eliminada exitosamente.')
        return redirect(next_url)
    
    context = {
        'experiencia': experiencia,
        'next_url': next_url,
    }
    return render(request, 'usuarios/confirmar_eliminar_experiencia.html', context)


# ============================================
# API: MUNICIPIOS POR DEPARTAMENTO
# ============================================

def obtener_municipios(request, departamento):
    """API para obtener municipios según el departamento seleccionado"""
    from perfiles.models import MUNICIPIOS_POR_DEPARTAMENTO
    
    municipios = MUNICIPIOS_POR_DEPARTAMENTO.get(departamento, [])
    return JsonResponse({'municipios': municipios})
