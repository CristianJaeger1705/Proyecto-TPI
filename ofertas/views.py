from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from ofertas.models import OfertaLaboral
from ofertas.forms import Ofertasform
from ofertas.utils import es_empresa
from .decorators import empresa_o_admin_required

# =====================================================
# LISTADO DE OFERTAS PÚBLICO Y PRIVADO
# =====================================================
def listado_ofertas(request):
    # Solo mostrar ofertas activas
    ofertas = OfertaLaboral.objects.filter(estado='activa').order_by('-fecha_publicacion')
    return render(request, 'ofertas/listado_ofertas.html', {'ofertas': ofertas})


def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id, estado='activa')
    return render(request, 'ofertas/detalle_oferta.html', {'oferta': oferta})


@login_required(login_url='login')
def ofertas_List(request):
    usuario = request.user

    if es_empresa(usuario):
        try:
            empresa = usuario.perfilempresa
        except:
            messages.error(request, "Tu cuenta de empresa no tiene perfil configurado.")
            return redirect("hola_mundo")
        ofert = OfertaLaboral.objects.filter(empresa=empresa).order_by('-fecha_publicacion')
    elif usuario.rol == "candidato":
        ofert = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    else:
        messages.error(request, "Tipo de usuario desconocido.")
        return redirect("hola_mundo")

    # Filtrado por ubicación
    ubicacion = request.GET.get('ubicacion')
    if ubicacion:
        ofert = ofert.filter(ubicacion__icontains=ubicacion)

    paginator = Paginator(ofert, 10)
    page_number = request.GET.get('page')
    ofertas = paginator.get_page(page_number)
    ubicaciones = ofert.values_list('ubicacion', flat=True).distinct()

    return render(request, 'ofertas/index.html', {
        'ofertas': ofertas,
        'ubicaciones': ubicaciones,
        'es_empresa': es_empresa(request.user)
    })


# =====================================================
# FORMULARIOS MODALES
# =====================================================
@login_required(login_url='login')
def obtener_formulario_creacion(request):
    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    formulario = Ofertasform()
    form_html = render(request, 'ofertas/form.html', {
        'formulario': formulario,
        'es_modal': True,
        'es_creacion': True
    }).content.decode('utf-8')

    return JsonResponse({'success': True, 'form_html': form_html})


@login_required(login_url='login')
def obtener_formulario_edicion(request, id):
    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    empresa = request.user.perfilempresa
    oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
    formulario = Ofertasform(instance=oferta)

    form_html = render(request, 'ofertas/form.html', {
        'formulario': formulario,
        'oferta': oferta,
        'es_modal': True,
        'es_creacion': False
    }).content.decode('utf-8')

    return JsonResponse({'success': True, 'form_html': form_html, 'titulo': oferta.titulo})


# =====================================================
# GUARDAR CREACIÓN Y EDICIÓN DESDE MODAL
# =====================================================
@login_required(login_url='login')
def guardar_creacion_modal(request):
    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        empresa = request.user.perfilempresa
        formulario = Ofertasform(request.POST, request.FILES)
        if formulario.is_valid():
            nueva_oferta = formulario.save(commit=False)
            nueva_oferta.empresa = empresa
            nueva_oferta.save()
            return JsonResponse({'success': True, 'message': f'Oferta "{nueva_oferta.titulo}" creada correctamente'})

        form_html = render(request, 'ofertas/form.html', {
            'formulario': formulario,
            'es_modal': True,
            'es_creacion': True
        }).content.decode('utf-8')

        return JsonResponse({'success': False, 'error': 'Por favor corrige los errores del formulario', 'form_html': form_html})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@login_required(login_url='login')
def guardar_edicion_modal(request, id):
    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        empresa = request.user.perfilempresa
        oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
        formulario = Ofertasform(request.POST, request.FILES, instance=oferta)

        if formulario.is_valid():
            oferta_guardada = formulario.save()
            return JsonResponse({'success': True, 'message': f'Oferta "{oferta_guardada.titulo}" actualizada correctamente'})

        form_html = render(request, 'ofertas/form.html', {
            'formulario': formulario,
            'oferta': oferta,
            'es_modal': True,
            'es_creacion': False
        }).content.decode('utf-8')

        return JsonResponse({'success': False, 'error': 'Por favor corrige los errores del formulario', 'form_html': form_html})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


# =====================================================
# ELIMINAR OFERTA
# =====================================================
@login_required(login_url='login')
def eliminar(request, id):
    if not es_empresa(request.user):
        messages.error(request, "No autorizado.")
        return redirect('ofertas:ofertas')

    empresa = request.user.perfilempresa
    oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
    oferta.delete()
    messages.success(request, "Oferta eliminada correctamente")
    return redirect('ofertas:ofertas')


# =====================================================
# VISUALIZAR OFERTA MODAL
# =====================================================
@login_required(login_url='login')
def obtener_datos_visualizacion(request, id):
    try:
        oferta = get_object_or_404(OfertaLaboral, id=id)
        acciones = {
            'puedePostular': puede_postular_con_id(request.user, id),
            'puedeCancelarPostulacion': puede_cancelar_postulacion(request.user, id),
        }
        form_html = render(request, 'ofertas/ofertview.html', {
            'oferta': oferta,
            'es_modal': True,
            'acciones': acciones
        }).content.decode('utf-8')
        return JsonResponse({'success': True, 'form_html': form_html, 'titulo': f"Visualizando: {oferta.titulo}"})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# =====================================================
# OFERTAS ABIERTAS AL PÚBLICO
# =====================================================
def lista_ofertas_publicas(request):
    ofertas = OfertaLaboral.objects.filter(estado='activa').order_by('-fecha_publicacion')
    contexto = {'ofertas': ofertas, 'total_ofertas': ofertas.count()}
    return render(request, 'ofertas/ofertas_publicadas.html', contexto)
